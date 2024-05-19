#!/bin/bash

docker load -i weather_image.tar
docker run -p 80:8989 -d --name weather-app weather:aws
