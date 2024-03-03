FROM python:3.12

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY trading/ /app/trading/

CMD ["uvicorn", "trading.main:asgi_app"]
