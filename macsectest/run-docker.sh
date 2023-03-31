#!/bin/bash
docker rm -f test
docker build -t test .
docker -D run --name test --env EXECUTION_CTX='docker' -it --privileged --net="host" -v /lib/modules:/lib/modules test
