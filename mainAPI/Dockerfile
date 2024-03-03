FROM python:3.12.2-alpine

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 8232

CMD ["python", "flaskApp.py"]