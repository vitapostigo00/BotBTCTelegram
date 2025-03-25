import requests
import re
#Imports propios
from conexionMongo import booleanFromUser
from credentials import get_credentials

def consultaNodoRPC(rpc_url,rpc_user,rpc_password,payload):
    try: 
        response = requests.post(rpc_url, auth=(rpc_user, rpc_password), json=payload)
        response.raise_for_status()
        jsonRetorno = response.json()
        return jsonRetorno
    except requests.exceptions.RequestException as e:
        return "Error"


# Método que queremos consultar
def infoBlockchain(user_id):
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual
    
    credentials = get_credentials(redActual)

    payload = {
        "jsonrpc": "1.0",
        "id": "test",
        "method": "getblockchaininfo",
        "params": []
    }

    jsonToParse = consultaNodoRPC(credentials["nodo"]["rpc_url"],credentials["nodo"]["rpc_user"],credentials["nodo"]["rpc_password"],payload)
    
    resultadoRed = jsonToParse.get("result", {}).get("chain", "Desconocido")

    if resultadoRed == "main":
        return "mainnet"
    elif resultadoRed == "test":
        return "testnet"
    else:
        return "undefined"


def infoTx(user_id,tx):
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual
    
    credentials = get_credentials(redActual)

    payload = {
        "jsonrpc": "1.0",
        "id": "test",
        "method": "gettransaction",
        "params": [str(tx),"true","true"]
    }

    #jsonToParse = consultaNodoRPC(credentials["nodo"]["rpc_url"],credentials["nodo"]["rpc_user"],credentials["nodo"]["rpc_password"],payload)

    #return jsonToParse






def precio_bitcoin():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return str(data['bitcoin']['usd'])


def precioPorBTC(num):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()

    valorEnDols = (data['bitcoin']['usd'])*num
    precio = "{:.2f}".format(valorEnDols)

    return str(precio)+ '$'


def isValidBTCAddress(address):
    regex = r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{24,39}$"
    return bool(re.match(regex, address))
    