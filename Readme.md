# Sistema de Alertas para Bitcoin en Telegram

ATENCIÓN: El proyecto está temporalmente parado aunque sigue siendo usable.
El nuevo proyecto en desarrollo que está usando el código de este proyecto es:
https://github.com/vitapostigo00/BlockchainConversationalAI

Todo el código se encuentra en el repositorio:
Existe un bot de Telegram disponible que usa este código.  
Para usarlo, simplemente busca en Telegram:

```
@AlertsBTCbot
```

y podrás utilizarlo libremente.

---

## Ejecución Local del Sistema

### Sincronización Inicial de los Nodos

La blockchain de Bitcoin puede descargarse en un equipo y luego trasladarse a otro.  
Para facilitar la gestión de permisos, se recomienda que la transferencia se realice entre sistemas Linux con discos formateados en **EXT4**.  
También es posible descargar la blockchain en Windows y luego trasladarla a Linux.

Las tres carpetas que deben copiarse y trasladarse son:

- `blocks`
- `chainstate`
- `indexes`

Estas deben ubicarse en el directorio correspondiente donde se ejecutarán los nodos.

> 💡 Si se utiliza un disco NTFS (Windows), asegúrate de tener instalado `ntfs-3g` en Linux para poder escribir en él correctamente.

Para que **Fulcrum** funcione correctamente, los nodos Bitcoin deben ejecutarse con la opción:

```
-txindex=1
```

Durante la sincronización inicial:

- No es necesario exponer puertos.
- Se deben modificar las rutas en los archivos Docker para apuntar a las ubicaciones correctas de los datos.

---

### Requisitos de Hardware

Se recomienda lo siguiente:

- HDD de al menos **2 TB** (para mainnet + testnet).
- SSD de **al menos 500 GB** para alojar los nodos y Fulcrum.

#### Opción 1: Sincronización desde otro equipo

- Almacena la blockchain (mainnet + testnet) en un **HDD externo**.
- Usa un **SSD** para las bases de datos de Fulcrum.

> Requisitos aproximados de espacio:
> - Fulcrum DB: ~430 GB
> - Mainnet: ~756 GB
> - Testnet: ~250 GB

#### Opción 2: Sincronización desde Raspberry Pi

- Usa un SSD externo de alto rendimiento.
- Todos los procesos accederán al mismo disco, así que la I/O será intensa.

> 💡 Lo ideal sería tener **2 SSDs**: uno para la blockchain y otro para Fulcrum.

En este sistema, se reutilizó un HDD externo de **8 TB @ 5400 RPM USB 3.0** para reducir costes.

Para acelerar la sincronización de Fulcrum se recomienda:

```
--utxo-cache=<memoria_en_MB>
```

---

### Orden Óptimo de Sincronización

1. Sincronizar primero el nodo **testnet**.
2. Iniciar Fulcrum para testnet y nodo **mainnet** simultáneamente.
3. Sincronizar Fulcrum para **mainnet**.

---

## Generación de Credenciales RPC

1. Usar el script `rpcauth.py` del repositorio oficial de Bitcoin.
2. Ejecutarlo con el nombre de usuario deseado:

```
rpcauth=mainnet:da33953f...$48986b...
Your password: ttKTQzCqIembZaBY_BRXYpLuZG0_i12Ud9lhRULs8xk
```

3. Repetir el proceso para **mainnet** y **testnet**.

> ⚠ Aunque los contenedores usan red interna de Docker, maneja estas credenciales con precaución.

### Ejemplo de variables en `variables.sh`

```bash
TESTNET_PASS="L0MeGILHo7m89uavaIlNv9nptsbc65D_863z45Y8mwM"
MAINNET_PASS="ttKTQzCqIembZaBY_BRXYpLuZG0_i12Ud9lhRULs8xk"
```

---

## API Key para el Bot de Telegram

1. Habla con `@BotFather`.
2. Ejecuta los comandos `/start` y `/newbot`.
3. Sigue las instrucciones y obtendrás una **API Key**.

---

## Creación de Archivos para los Contenedores

En cada carpeta del directorio `containers/`, crea un archivo `ApiToken.py`:

```python
def returnApiToken():
    return ApiKey

def btcMainnetPass():
    return MainnetPass

def btcTestnetPass():
    return TestnetPass
```

Sustituye las variables `ApiKey`, `MainnetPass` y `TestnetPass` por tus valores.

Crea también el script `rebuildContainers.sh` y ejecútalo con:

```
./rebuildContainers.sh
```

> Si hay problemas de permisos:

```
chmod +x script.sh
```

Una vez los contenedores estén compilados y los nodos sincronizados:

- Iniciar: `./lanzar.sh`
- Detener: `./parar.sh`

> ⚠ No usar `lanzar.sh` hasta haber completado toda la configuración.

---

## Configuración de Usuarios en MongoDB

Para distinguir entre mainnet y testnet:

1. Ejecuta MongoDB:

```
docker exec -it mongo_db mongosh
```

2. Introduce los comandos:

```javascript
use telegram_bot
db.createCollection("direcciones")
db.createCollection("cuentasTelegram")
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
```

Esto crea la base de datos y los dos usuarios "base".

---

## Creación de Subred Docker

Ejecuta:

```
docker network create --driver=bridge --subnet=192.168.33.0/24 --gateway=192.168.33.1 botTelegram
```

Esto crea la red Docker `botTelegram` con el rango IP definido.

---

Con esto, el sistema estará preparado para funcionar correctamente 🚀
