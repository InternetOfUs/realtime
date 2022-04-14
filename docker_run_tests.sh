#! /bin/sh
docker run -v $(pwd):/app docker.idiap.ch/wenet/wenet-realtime ./run_tests.sh $@