#!/bin/bash
while true
do
    echo --- WIPE DAEMON CLEANS DOCKER ---
    sudo docker stop bar00 bar01 bar02
    sudo docker rm -f "$(sudo docker ps -aq)"
    sudo docker rmi -f "$(sudo docker images -q)"
    sudo docker system prune -a -f

    echo --- WIPE DAEMON BUILDS DOCKER ---
    sudo docker build -t foo0 .

    echo --- WIPE DAEMON RUNS DOCKER ---
    sudo docker run --rm -t -d --name bar00 foo0
    sudo docker run --rm -t -d --name bar01 foo0
    sudo docker run --rm -t -d --name bar02 foo0

    SLEEP=$((1800 + RANDOM % 3600))
    SLICE=$((SLEEP / 10))

    for (( i = 0; i <= 10; i++ )); do

        echo --- WIPE DAEMON SLEEPS "$SLICE"S ---
        sleep "$SLICE"

        CONTAINERS=$(sudo docker ps -aq | tr '\n' ' ')
        if [ "$CONTAINERS" ]; then
            echo --- "$CONTAINERS"ARE STILL ALIVE ---
            continue
        else
            echo --- NO CONTAINERS FOUND, BREAKING ---
            break
        fi

    done

done


