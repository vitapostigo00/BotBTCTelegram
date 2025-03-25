import hashlib
import bitcoinlib
from bitcoinlib.transactions import Output
from ApiToken import btcMainnetPass,btcTestnetPass,ipLocal

#Para mongodb:
#Mirar para cambiar las ips por redes internas.
credsMongo = {
    "client": "mongodb://192.168.1.184:27017/",
    "db": "telegram_bot",
    "collection": "seguimientos"
}

#MAINNET: 
credsNodoMainnet = {
    "rpc_user" : "mainnet",
    "rpc_password" : btcMainnetPass(),
    "rpc_url" : "http://"+ipLocal()+":8332/"    
}

credsFulcrumMainnet = {
    "host" : '192.168.1.184',
    "port" : 50001
}

#TESTNET: 
credsNodoTestnet = {
    "rpc_user" : "testnet",
    "rpc_password" : btcTestnetPass(),
    "rpc_url" : "http://"+ipLocal ()+":18332/"
}

credsFulcrumTestnet = {
    "host" : ipLocal (),
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
def addr2scripthash(address):
    #Convierte la dirección en Script2Key para que el nodo pueda usarla.
    script = Output(0, address).script
    script_bytes = script.serialize()
    hash_value = hashlib.sha256(script_bytes).digest()
    reversed_hash = hash_value[::-1]
    return reversed_hash.hex()

#Consultas a nodo Fulcrum
def getFulcrumQuery(method,data):
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
                "params": [addr2scripthash(data)],
                "id": 0
            }
        elif method == 'firstUse':
            return { #Data debera ser una direccion
                "method": "blockchain.scripthash.get_first_use",
                "params": [addr2scripthash(data)],
                "id": 0
            }
        elif method == 'getHistory':
            return { #Data debera ser una direccion
                "method": "blockchain.scripthash.get_history",
                "params": [addr2scripthash(data),0,-1],
                "id": 0
            }
        else:
            return {}
        
    except bitcoinlib.encoding.EncodingError as e:
        return {}


