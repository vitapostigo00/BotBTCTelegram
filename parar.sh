#Muchas veces los contenedores al ser relativamente pesados, presentan corrupción en las bases de datos al cerrar con docker stop.
#Este script permite cerrarlos de manera más controlada usando kill -SIGINT <PID> de manera que no tendremos este problema.
if ! docker info &>/dev/null; then
    echo "Docker no está en ejecución o no tienes permisos."
    exit 1
fi

# Obtener la lista de contenedores en ejecución
containers=$(docker ps -q)

if [ -z "$containers" ]; then
    echo "No hay contenedores en ejecución."
    exit 0
fi

echo "Enviando SIGINT a todos los contenedores..."

for container in $containers; do
    docker exec -it "$container" bash -c 'kill -SIGINT 1'
done

echo "Proceso completado."