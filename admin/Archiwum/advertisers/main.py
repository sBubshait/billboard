from __future__ import annotations

from quart import Quart
from quart import request
from quart import render_template
from httpx import AsyncClient

from advertisers import settings

async def render_page(
    path: str,
    title: str,
    error: str | None = None,
    success: str | None = None,
    warning: str | None = None,
    **kwargs,
) -> str:
    # This might be a bit unsafe for social engineering but oh wellll.
    success = success or request.args.get("success")
    error = error or request.args.get("error")
    warning = warning or request.args.get("warning")

    return await render_template(
        path,
        title=title,
        success=success,
        error=error,
        warning=warning,
        settings=settings,
        **kwargs,
    )


def configure_routes(app: Quart) -> None:
    @app.route("/", methods=["GET", "POST"])
    async def index() -> str:
        success = None
        error = None
        if request.method == "POST":
            form = await request.form
            url = form["ad_url"]

            # Preferences
            food_category = float(form["food_category"])
            clothing_category = float(form["clothing_category"])
            electronics_category = float(form["electronics_category"])
            entertainment_category = float(form["entertainment_category"])
            health_category = float(form["health_category"])
            beauty_category = float(form["beauty_category"])
            automotive_category = float(form["automotive_category"])
            home_category = float(form["home_category"])

            budget = float(form["budget"])

            # Server side validation.
            if budget < 0:
                error = "Budget must be a positive number."
            
            elif all(
                category <= 0
                for category in [
                    food_category,
                    clothing_category,
                    electronics_category,
                    entertainment_category,
                    health_category,
                    beauty_category,
                    automotive_category,
                    home_category,
                ]
            ):
                error = "At least one category must have a positive value."

            # Normalise all the preferences.
            total = sum(
                [
                    food_category,
                    clothing_category,
                    electronics_category,
                    entertainment_category,
                    health_category,
                    beauty_category,
                    automotive_category,
                    home_category,
                ]
            )

            food_category /= total
            clothing_category /= total
            electronics_category /= total
            entertainment_category /= total
            health_category /= total
            beauty_category /= total
            automotive_category /= total
            home_category /= total

            if not error:
                async with AsyncClient() as client:
                    response = await client.post(
                        f"{settings.API_URL}/putAd/",
                        json={
                            "name": "Advertiser Panel",
                            "budget": budget,
                            "bid": budget,
                            "url": url,
                            "adType": 0,
                            "health_preferences": health_category,
                            "food_preferences": food_category,
                            "clothing_preferences": clothing_category,
                            "electronics_preferences": electronics_category,
                            "entertainment_preferences": entertainment_category,
                            "beauty_preferences": beauty_category,
                            "home_preferences": home_category,
                            "automative_preferences": automotive_category,
                            "other_preferences": 0
                        }
                    )
                    
                    print(response.text)
                    if response.status_code not in range(200, 300):
                        error = f"Failed to place bid: {response.text}"
                    else:
                        success = f"Your bid for £{budget:.2f} has been placed!"


        return await render_page(
            "form.html", 
            "Bid",
            success=success,
        )

def create_app() -> Quart:
    app = Quart(
        __name__,
        static_folder="../static",
        template_folder="../templates",
    )

    configure_routes(app)


    return app


wsgi_app = create_app()
