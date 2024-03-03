FROM python:3.12.2-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements/main.txt

EXPOSE 8000

CMD ["uvicorn", "advertisers.main:wsgi_app", "--host", "0.0.0.0"]