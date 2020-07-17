# wenet-realtime

real-time API for the wenet project.

## Install

install the requirements

> pip install -r requirements.txt

## Run

Local server can be run with 

> uvicorn wenet_realtime.app:app

## Testing

> DEFAULT_DB_URL="sqlite:///:memory:" python3 -m unittest discover -s wenet_realtime

## Docs

On the route */docs* once the server is running