#!/bin/bash

base_path="ESCRIBIR AQUI EL PATH DE LA CARPETA CONTAINERS"

IMAGE_NAME_1="bot_telegram_btc"
IMAGE_NAME_2="zmq_listener"

PATH_1="${base_path}/bot_telegram_btc"
PATH_2="${base_path}/zmq_listener"

cp ${base_path}/ApiToken.py ${PATH_1}/ApiToken.py
echo "Building $IMAGE_NAME_1..."
docker build --no-cache -t $IMAGE_NAME_1 $PATH_1
rm ${PATH_1}/ApiToken.py

cp ${base_path}/ApiToken.py ${PATH_2}/ApiToken.py
echo "Building $IMAGE_NAME_2..."
docker build --no-cache -t $IMAGE_NAME_2 $PATH_2
rm ${PATH_2}/ApiToken.py

echo "Build completed."