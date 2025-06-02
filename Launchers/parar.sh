#!/bin/bash

if ! docker info &>/dev/null; then
    echo "Docker no está en ejecución o no tienes permisos."
    exit 1
fi

containers=$(docker ps -q)

if [ -z "$containers" ]; then
    echo "No hay contenedores en ejecución."
    exit 0
fi

echo "Enviando SIGINT a todos los contenedores..."

for container in $containers; do
    docker exec -it "$container" bash -c 'kill -SIGINT 1'
done

docker stop zmq_listener &>/dev/null

echo "Proceso completado."