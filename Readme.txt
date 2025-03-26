Se recomienda usar un SSD de 2 TB (o 2 de 1TB para una sincronización más rápida).

Para las primera sincronización, no es necesario publicar ningún tipo de puerto y hay que editar las rutas de docker usadas (para los voúmenes montados).
En caso de usar un HDD (minimo 1TB, si son 2 mejor ya que pronto entre mainnet y testnet ocuparán más) y un SSD (minimo 500Gb), los nodos deberán ir en el SSD y Fulcrum en el SSD.
Se recomienda usar el parámetro --utxo-cache con la memoria (en MB que se quiera asignar) para acelerar la sincronización inicial de Fulcrum.
En esta configuración de discos, el orden más óptimo para acelerar la sincronización de todos los datos (puede durar semana y media/2 semanas) es sincronizar primero el nodo de testnet,
una vez sincronizado, sincronizar a la vez fulcrum en testnet y el nodo de mainnet y finalmente sincronizar fulcrum con la mainnet.

Los contenedores usados son los que se muestran a continuación:
https://hub.docker.com/r/bitcoin/bitcoin
https://hub.docker.com/r/cculianu/fulcrum

Para obtener una API key propia para el bot de Telegram:
https://stackoverflow.com/questions/43291868/where-to-find-the-telegram-api-key

El proyecto se encuentra aún en desarrollo, una vez desarrollado y escrito el código se generará un contenedor para desplegar el bot más fácilmente pero aún se está lejos de ese punto.
También se hará una setup-guide para configurar las redes internas de docker exponiendo los puertos lo menos posible.

Librerías de interés usadas:
https://github.com/jgarzik/python-bitcoinrpc