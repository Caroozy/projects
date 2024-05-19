#!/bin/bash

docker stop weather-app
docker rm weather-app
docker system prune -f
