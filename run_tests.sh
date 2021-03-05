#! /bin/bash
coverage run --source=wenet_realtime -m unittest discover -s wenet_realtime && coverage report