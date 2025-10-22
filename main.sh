#!/bin/bash

RUN_SERVER=1
while [ "$#" -gt "0" ]
do
    case $1 in
        "--no-server")
            RUN_SERVER=0
            ;;
        "--server")
            RUN_SERVER=1
            ;;
        *)
            echo Invalid argument: $1
            exit 1
            ;;
    esac
    shift
done

python3 src/main.py || exit 1

if [ "$RUN_SERVER" -gt "0" ]
then
    echo "Running server"
    python3 -m http.server 8888 -d public
else
    echo "Not running server"
fi
