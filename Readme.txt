Existe un bot de Telegram disponible para consultar en Telegram que usa este código.
Para usarlo simplemente buscar en Telegram a:
"@AlertsBTCbot" y desde ahí se puede usar libremente.

En caso de querer ejecutar el sistema localmente, el proceso a seguir es el siguiente:
Sincronización inicial de los nodos
La blockchain de Bitcoin puede descargarse en un equipo y luego trasladarse a otro. Para facilitar la gestión de permisos, se recomienda que la transferencia se realice entre sistemas Linux con discos formateados en EXT4. Sin embargo, también es posible descargar la blockchain en un nodo Bitcoin bajo Windows y posteriormente trasladarla a un sistema Linux.

Las tres carpetas que deben copiarse y trasladarse son: blocks, chainstate e indexes. Estas deben ubicarse en el directorio correspondiente donde se ejecutarán los nodos.
En caso de utilizar un disco formateado en NTFS (típico de Windows), es imprescindible asegurarse de que Linux tenga instalado el paquete ntfs-3g para poder escribir correctamente en el sistema de archivos.
Para que Fulcrum funcione correctamente, los nodos Bitcoin deben ejecutarse con la opción -txindex=1, que habilita el índice de transacciones.

Durante la sincronización inicial no es necesario exponer puertos de red; además, es preciso modificar las rutas en los archivos Docker que definen los volúmenes montados para que apunten a las ubicaciones correctas de los datos.

Respecto al hardware, si se dispone de un disco duro mecánico (HDD) con una capacidad mínima recomendada de 1 TB (idealmente 2 TB, ya que la combinación de mainnet y testnet puede superar este espacio) y un disco de estado sólido (SSD) de al menos 500 GB, se recomienda alojar los nodos Bitcoin en el SSD para acelerar su rendimiento, así como los servicios Fulcrum. Existen 2 opciones con el equipo previamente elegido:

Sincronización mediante la ayuda de un dispositivo externo
Si se dispone de otro equipo con SSD que permita realizar la sincronización inicial de la blockchain, se recomienda utilizar un disco duro externo (HDD) para almacenar las blockchains (mainnet y testnet), y un SSD para alojar la base de datos que utiliza Fulcrum. Actualmente, Fulcrum requiere aproximadamente 430 GB para sus dos bases de datos, mientras que la mainnet de Bitcoin ocupa unos 756 GB y la testnet unos 250 GB. En consecuencia, lo más adecuado es utilizar un HDD de al menos 2 TB para el almacenamiento de las blockchains, y un SSD de 1 TB para la base de datos de Fulcrum.

Sincronización local usando solo la placa Raspberry Pi
En caso de no contar con otro equipo, se puede realizar la sincronización directamente en un SSD externo. Es fundamental que se utilice una unidad SSD de alto rendimiento, ya que el proceso de sincronización es muy exigente en términos de I/O. En este caso, todos los procesos del sistema estarán accediendo simultáneamente al mismo disco, lo que impide distribuir la carga.

El escenario óptimo sería disponer de dos unidades SSD (una para la blockchain y otra para la base de datos) y realizar la sincronización desde un equipo externo. No obstante, para este sistema se ha reutilizado un disco duro externo de 8 TB a 5400 RPM con interfaz USB 3.0 que ya estaba disponible, lo cual ha permitido reducir costes sin comprometer la funcionalidad básica del sistema.
Para optimizar la sincronización inicial de Fulcrum, se aconseja usar el parámetro --utxo-cache con la cantidad de memoria en megabytes que se quiera asignar. Esto mejora significativamente la velocidad de sincronización.

El orden óptimo para acelerar la sincronización, que puede durar entre una semana y semana y media, es el siguiente:
1.	Sincronizar primero el nodo de testnet.
2.	Una vez completada la sincronización del nodo de testnet, iniciar simultáneamente Fulcrum para testnet y el nodo de mainnet.
3.	Finalmente, sincronizar Fulcrum para mainnet.

Generación de credenciales RPC para la comunicación entre nodos
Para obtener el usuario y la contraseña necesarios para la comunicación RPC entre los nodos y Fulcrum, se debe realizar lo siguiente:
1.	Acceder al script rpcauth.py disponible en el repositorio oficial de Bitcoin [13].
2.	Copiar el contenido del archivo y pegarlo en un entorno que permita ejecutar código Python. Se recomienda usar un entorno local pero, en caso de no disponer de él, se puede usar un compilador online.
3.	Ejecutar el script pasando como argumento el nombre de usuario deseado para la conexión. Este proceso genera un valor de autenticación rpcauth y una contraseña asociada que cambia en cada ejecución.
Por ejemplo, al usar el nombre de usuario mainnet, se puede obtener una salida similar a:
rpcauth=mainnet:da33953f8f418795759903233e7cc025$48986b73421c74a88e692206c3a15af0b94850ead693d95554d400bf6b4531e9
Your password: ttKTQzCqIembZaBY_BRXYpLuZG0_i12Ud9lhRULs8xk
Este procedimiento debe repetirse para generar las credenciales tanto de Mainnet como de Testnet.

Aunque estas credenciales no son extremadamente sensibles debido a que los contenedores se comunican únicamente a través de la red interna de Docker, se recomienda manejarlas con precaución.

El valor rpcauth generado se utilizará en el script lanzar.sh para configurar la autenticación RPC, mientras que la contraseña que aparece en "Your password" será empleada por Fulcrum y almacenada en el archivo variables.sh con un formato similar al siguiente:

TESTNET_PASS="L0MeGILHo7m89uavaIlNv9nptsbc65D_863z45Y8mwM"
MAINNET_PASS="ttKTQzCqIembZaBY_BRXYpLuZG0_i12Ud9lhRULs8xk"
(Las contraseñas mostradas son ejemplos)

8.3 Obtención de la API KEY para el Bot en Telegram
Para compilar los contenedores y utilizar un bot propio, es necesario obtener una clave API (API Key). Este proceso es sencillo y se realiza a través de Telegram, buscando el usuario oficial llamado BotFather y ejecutando la siguiente secuencia de comandos:
/start	y /newbot

A continuación, se deberá proporcionar un nombre interno que identifique al bot dentro de nuestro sistema, seguido del nombre público del bot, el cual debe finalizar con la palabra “bot”.

Después de completar estos pasos, BotFather enviará un mensaje que incluye la clave API necesaria para interactuar con el bot.

Generación de ficheros para la creación de los containers
Una vez obtenida esta clave, se procederá a crear la estructura de carpetas mencionada anteriormente bajo el directorio containers. En cada una de estas carpetas se copiarán los correspondientes archivos Dockerfile, asegurándose de que el entry point sea el correcto, es decir, que corresponda al bot propio o al servicio zmq_listener, según corresponda.

En cada carpeta será necesario crear un archivo llamado ApiToken.py, que debe tener la siguiente estructura básica:

def returnApiToken():
    return ApiKey

def btcMainnetPass():
    return MainnetPass

def btcTestnetPass():
    return TestnetPass
En este archivo se deberán reemplazar las variables ApiKey, MainnetPass y TestnetPass por los valores correspondientes, incluyendo la clave API recién obtenida. Este procedimiento se debe realizar en ambas carpetas de contenedores.

Finalmente, se debe crear el script rebuildContainers.sh, modificando las rutas para que apunten correctamente a la ubicación donde se encuentra la estructura de carpetas en el sistema.

Para construir los contenedores, se ejecutará el script mediante:
./rebuildContainers.sh

Si la ejecución no es posible debido a problemas de permisos, se recomienda cambiar los permisos de ejecución de los archivos correspondientes con el siguiente comando:
“chmod +x script.sh”
Esto permitirá otorgar permisos de ejecución a los scripts necesarios.

Una vez que los contenedores estén correctamente compilados y desplegados, y siempre que los nodos Bitcoin y Fulcrum estén sincronizados, se podrá iniciar el sistema con el comando
./lanzar.sh y detenerlo de forma ordenada utilizando: ./parar.sh
No obstante, hay que terminar la inicialización completa del sistema por tanto no se debe usar lanzar hasta haber acabado este apartado por completo.

Configuración de usuarios base para MongoDB
Para mayor simplicidad en el código del sistema, existen algunas consultas que se realizan directamente a la Blockchain. Por ejemplo, para notificar al usuario cuando existe un movimiento de fondos hace falta “hacerle saber” al programa si la dirección consultada se encuentra en Mainnet o Testnet.Para poder reutilizar el código donde se pasa por parámetro un usuario y no tener que volver a escribir un código muy similar, se han insertado 2 usuarios con unas ids que no pueden tener ninguna cuenta de Telegram. Estos son los usuarios con _id = 0 y _id = 1, los cuales están siempre (y no se pueden cambiar) en Mainnet y testnet respectivamente. Por ejemplo, en el código de zmq_listener se ve cómo cuando se publica un bloque en testnet se llama a:
actualBalance = getBalanceNode(str(1),cuenta["address"]) mientras que cuando este se publica en Mainnet se llama a:
actualBalance = getBalanceNode(str(0),cuenta["address"]).
Para registrar a ambos usuarios y estructurar la base de datos haremos lo siguiente:
Una vez el container de MongoDB se encuentre en ejecución, escribiremos:
docker exec -it mongo_db mongosh 
Con este commando podremos interactuar con MongoDB mediante CLI y podremos estructurar la base de datos a nuestra conveniencia.
Escribiremos los siguientes comandos uno detrás de otro:
use telegram_bot
db.createCollection(“direcciones”)
db.createCollection(“cuentasTelegram”)
db.cuentasTelegram.insertMany([
  {
    _id: "0",
    boolean_field: false,
    list_mainnet: [],
    list_testnet: []
  },
  {
    _id: "1",
    boolean_field: true,
    list_mainnet: [],
    list_testnet: []
  }
])
Con estos 4 comandos, creamos la base de datos, las 2 colecciones e insertamos ambos usuarios mencionados anteriormente.
Con esto, el sistema estará preparado para empezar a funcionar.


Creación de una subred de Docker
El último paso será crear una red de comunicación entre los contenedores. En este caso la red de ha llamado: “botTelegram” y se eligió el rango: 192.168.33.0/24.
La creación de esta red se hará escribiendo el comando:
“docker network create --driver=bridge --subnet=192.168.33.0/24 --gateway=192.168.33.1 botTelegram”
