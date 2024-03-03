import requests
from flask import Flask, Response, request, jsonify, render_template

ADS_API_URL = "https://api.c4s.lol/api/ads"
USERS_API_URL = "https://api.c4s.lol/api/users"
DEFAULT_AD_URL = "https://images-ext-1.discordapp.net/external/ww-yV5ZDyWrUUfl8l-67Ws_ENMlue-5N3FgGICQ5FV4/%3Fe%3D2147483647%26v%3Dbeta%26t%3Dai60QCmo_Q9up7y0Pwp3nYikv7phNq_R_Ur6B1vgQYM/https/media.licdn.com/dms/image/D4E10AQHKVyBIJ7aOzA/image-shrink_800/0/1707544834995?format=webp&width=1600&height=834"

app = Flask(__name__)


def get_current_ad_url() -> str:
    """
    Retrieve the current advertisement URL.

    :return: Advertisement URL
    """
    return app.config.get('CURRENT_AD_URL', DEFAULT_AD_URL)


def set_current_ad_url(url: str) -> None:
    """
    Set the current advertisement URL.

    :param url: Advertisement URL
    """
    app.config['CURRENT_AD_URL'] = url


def calculate_ad_score(ad_preferences: dict[str, float], user_averages: dict[str, float]) -> float:
    """
    Calculates the score of an advertisement based on the preferences and user weights.


    :param ad_preferences: A dictionary containing the ad preferences with keys as the theme names
                            and values as their corresponding weights.
    :param user_averages: A dictionary containing the user averages with keys as the theme names
                            and values as their corresponding weights.

    :return: The calculated score for the advertisement.
    """
    return sum(float(ad_preferences.get(key, 0)) * float(user_averages.get(key, 0)) for key in ad_preferences)


def get_best_ad_url(ads: dict, user_weights: dict) -> str:
    """
    Determines the best advertisement URL based on the provided ads data and user weights.

    :param ads: A dictionary containing a list of ads with their data and preferences.
    :param user_weights: A dictionary containing the average user weights of themes.

    :return: The URL of the ad with the highest score or the default.
    """
    best_ad, highest_score = "", 0
    for ad in ads.get('data', []):
        ad_score = calculate_ad_score(ad.get('preferences', {}), user_weights.get('averages', {}))
        if ad_score > highest_score:
            best_ad, highest_score = ad['url'], ad_score
    return best_ad or DEFAULT_AD_URL


@app.route('/sensor', methods=['POST'])
def handle_sensor_data() -> (str, int):
    """
    Endpoint to handle sensor data. Receives the current active users and determines the best ad to display.

    :return: A simple 'OK' response with a 200 status code.
    """
    users = request.json.get('users')

    if users:
        try:
            ads_response = requests.get(ADS_API_URL)
            ads_response.raise_for_status()
            ads = ads_response.json()

            user_weights_response = requests.post(USERS_API_URL, json={"codes": users})
            user_weights_response.raise_for_status()
            user_weights = user_weights_response.json()

            if ads.get('status') and user_weights.get('status'):
                set_current_ad_url(get_best_ad_url(ads, user_weights))
            else:
                set_current_ad_url(DEFAULT_AD_URL)
        except requests.RequestException as e:
            print(f"Network error: {e}")
    else:
        print('No users found in the request')

    return 'OK', 200


@app.route('/ad')
def serve_ad() -> str:
    """
    Endpoint to serve the advertisement HTML template.

    :return: The rendered advertisement template as an HTML response.
    """
    return render_template('template.html', ad_url=get_current_ad_url())


@app.route('/current-ad/')
def display_current_ad() -> Response:
    """
    Endpoint to get the current advertisement's URL.

    :return: A JSON response containing the URL of the current advertisement.
    """
    return jsonify({"url": get_current_ad_url()})


def run_app() -> None:
    """
    Runs the Flask application.
    """
    app.run(port = 8232, host = "0.0.0.0")


if __name__ == '__main__':
    run_app()
