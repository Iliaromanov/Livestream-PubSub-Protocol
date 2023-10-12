#!/bin/bash

# Usage eg: ./create_container.sh producer1

ip=$1

docker create -ti --name "$ip" --cap-add=all -v /Users/iromanov/Desktop/Networks/A1/Captures:/wrkdir live-protocol /bin/bash
docker network connect csnet "$ip"
docker cp /Users/iromanov/Desktop/Networks/A1/Livestream-PubSub-Protocol/Project "$ip":/wrkdir
