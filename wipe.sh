#!/bin/bash
while true
do
    echo ***WIPE DAEMON CLEANS DOCKER
    sudo docker rm -f $(sudo docker ps -aq)
    sudo docker rmi -f $(sudo docker images -q)
    sudo docker system prune -a -f

    echo ***WIPE DAEMON BUILDS DOCKER
    sudo docker build -t foo0 .

    echo ***WIPE DAEMON RUNS DOCKER
    sudo docker run --rm -t -d foo0

#    sudo docker logs --follow $(sudo docker ps -aq)
    SLEEP=$((3600 + $RANDOM % 10000))
    echo ***WIPE DAEMON SLEEPS $SLEEP s...
    sleep $(echo $SLEEP)

done


