FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY wenet_realtime wenet_realtime

RUN DEFAULT_DB_URL="sqlite:///:memory:" python3 -m unittest discover -s wenet_realtime

EXPOSE 8000

CMD ["uvicorn", "wenet_realtime.app:app"]