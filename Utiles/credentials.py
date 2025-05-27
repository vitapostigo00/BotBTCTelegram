import hashlib
import bitcoinlib
from bitcoinlib.transactions import Output
from ApiToken import *
from StaticIps import * 

#Para mongodb:
#Mirar para cambiar las ips por redes internas.
credsMongo = {
    "client": f"mongodb://{mongo_db()}:27017/",
    "db": "telegram_bot",
    "collection": "cuentasTelegram"
}

#MAINNET:
credsNodoMainnet = {
    "rpc_user" : "mainnet",
    "rpc_password" : btcMainnetPass(),
    "rpc_url" : f"http://{bitcoin_mainnet()}:8332/"
}

credsFulcrumMainnet = {
    "host" : fulcrum_mainnet(),
    "port" : 50001
}

#TESTNET:
credsNodoTestnet = {
    "rpc_user" : "testnet",
    "rpc_password" : btcTestnetPass(),
    "rpc_url" : f"http://{bitcoin_testnet ()}:18332/"
}

credsFulcrumTestnet = {
    "host" : fulcrum_testnet(),
    "port" : 50002
}

#Si es un booleano, erá 1 para testnet y 0 para mainnet
#Si es un string, será mongo para los datos de mongo
#En cualquier otro caso, devolvemos vacio.
def get_credentials(controlData):
    if not isinstance(controlData,bool):
        if controlData == 'mongo':
            return credsMongo
        else :
            return {}

    else:
        if controlData:
            return {
                "nodo": credsNodoTestnet,
                "fulcrum": credsFulcrumTestnet
            }
        else:
            return {
                "nodo": credsNodoMainnet,
                "fulcrum": credsFulcrumMainnet
            }

#Esta función está aqui (y no en funciones) para resolver los problemas de los imports circulares.
def addr2scripthash(address,testnet):
    #Convierte la dirección en Script2Key para que el nodo pueda usarla.
    if(testnet):
        script = Output(0, address,network='testnet').script
    else:
        script = Output(0, address).script
    script_bytes = script.serialize()
    hash_value = hashlib.sha256(script_bytes).digest()
    reversed_hash = hash_value[::-1]
    return reversed_hash.hex()

#Consultas a nodo Fulcrum
def getFulcrumQuery(method,data,testnet):
    if method == 'getTx':
        return { #Data debera ser una transacción
            "method": "blockchain.transaction.get",
            "params": [data, False],
            "id": 0
        }
    elif method == 'getBlockHash':
        return { #Data debera ser una transacción
            "method": "blockchain.transaction.get_confirmed_blockhash",
            "params": [data,False],
            "id": 0
        }
    try:
        if method == 'getBalance':
            return { #Data debera ser una direccion
                "method": "blockchain.scripthash.get_balance",
                "params": [addr2scripthash(data,testnet)],
                "id": 0
            }
        elif method == 'firstUse':
            return { #Data debera ser una direccion
                "method": "blockchain.scripthash.get_first_use",
                "params": [addr2scripthash(data,testnet)],
                "id": 0
            }
        elif method == 'getHistory':
            return { #Data debera ser una direccion
                "method": "blockchain.scripthash.get_history",
                "params": [addr2scripthash(data,testnet),0,-1],
                "id": 0
            }
        elif method == 'blockFromTx':
            return { #Data debera ser una transacción
                "method": "blockchain.transaction.get_height",
                "params": [data],
                "id": 0
            }
        elif method == 'blockHashFromHeight':
            return { #Data debera ser un numero
                "method": "blockchain.block.header",
                "params": [data,0],
                "id": 0
            }
        else:
            return {}

    except bitcoinlib.encoding.EncodingError as e:
        return {}

#PARTE DE PRUEBAS PARA NO TENER QUE CONSULTAR EL NODO RPC A MANO:
def getMainnetClient():
    return f"http://mainnet:{btcMainnetPass()}@{bitcoin_mainnet()}:8332"

def getTestnetClient():
    return f"http://testnet:{btcTestnetPass()}@{bitcoin_testnet()}:18332"