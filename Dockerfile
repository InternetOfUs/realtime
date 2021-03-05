FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY wenet_realtime wenet_realtime
COPY *.sh .

RUN DEFAULT_DB_URL="sqlite:///:memory:" python3 -m unittest discover -s wenet_realtime

EXPOSE 8000
ENV DEFAULT_DB_URL="sqlite:///:memory:"
CMD ["uvicorn", "--host", "0.0.0.0", "--workers", "1", "wenet_realtime.app:app"]