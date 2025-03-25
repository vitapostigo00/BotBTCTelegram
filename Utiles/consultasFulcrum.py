import socket
from time import sleep
import json
import bitcoinlib
from conexionMongo import booleanFromUser
from credentials import get_credentials, getFulcrumQuery

def consultaFulcrum(host, port, content):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(json.dumps(content).encode('utf-8')+b'\n')
    sleep(0.5)
    sock.shutdown(socket.SHUT_WR)
    res = ""
    while True:
        data = sock.recv(1024)
        if (not data):
            break
        res += data.decode()
    sock.close()
    return res
    
""" Se mueve directamente al nodo:
def getTxInfo(user_id,tx):
    #No está terminado, probablemente haya que pasarlo a decoderawtransaction. Por ahora dejarlo para el final
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual

    jsonQuery = getFulcrumQuery('getTx',tx)
    servidor = get_credentials(redActual)

    try:
        respuesta = consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery)
        
        #A veces el servidor no responde correctamente, esto no suele pasar pero lo reintentamos
        if not respuesta:     
            for i in range(3):
                respuesta = consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery)
                if respuesta:
                    break
                else:
                    sleep(1)
        
        #Ahora se pueden dar 3 casos, que hayamos obtenido respuesta, que obtengamos un error o que todo se haya obtenido correctamente.
        if not respuesta:
            #Si no tenemos respuesta, no podemos parsear el json, devolvemos error del servidor por pantalla
            return "Error de conexion al servidor."

        if 'error' in respuesta:
            return "No se ha podido encontrar la transacción en la red seleccionada."      

        data = json.loads(respuesta)
        return data

        
    except bitcoinlib.encoding.EncodingError as e:
        return "La dirección no tiene un formato correcto."
"""
    

def getBlockFromTx(user_id,tx):
    #Mirar cómo queremos los campos en el bot de Telegram
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual

    jsonQuery = getFulcrumQuery('getBlockHash',tx)
    servidor = get_credentials(redActual)

    try:
        respuesta = consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery)
        #A veces el servidor no responde correctamente, esto no suele pasar pero lo reintentamos
        if not respuesta:     
            for i in range(3):
                respuesta = consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery)
                if respuesta:
                    break
                else:
                    sleep(1)
        
        #Ahora se pueden dar 3 casos, que hayamos obtenido respuesta, que obtengamos un error o que todo se haya obtenido correctamente.
        if not respuesta:
            #Si no tenemos respuesta, no podemos parsear el json, devolvemos error del servidor por pantalla
            return "Error de conexion al servidor."

        if 'error' in respuesta:
            return "No se ha podido encontrar la transacción en la red seleccionada."      

        data = json.loads(respuesta)
        return data

        
    except bitcoinlib.encoding.EncodingError as e:
        return "La dirección no tiene un formato correcto."
    
def getBalanceNode(user_id,address):
    satsInBTC = 100000000
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual

    jsonQuery = getFulcrumQuery('getBalance',address)
    servidor = get_credentials(redActual)

    try:
        data = json.loads(consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery))
        confirmed = float(data['result']['confirmed'])
        return confirmed/satsInBTC
    
    except bitcoinlib.encoding.EncodingError as e:
        return "La dirección no tiene un formato correcto."
    

def firstUse(user_id,tx):
    #Mirar cómo queremos los campos en el bot de Telegram
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual

    jsonQuery = getFulcrumQuery('firstUse',tx)
    servidor = get_credentials(redActual)

    try:
        respuesta = consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery)
        #A veces el servidor no responde correctamente, esto no suele pasar pero lo reintentamos
        if not respuesta:     
            for i in range(3):
                respuesta = consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery)
                if respuesta:
                    break
                else:
                    sleep(1)
        
        #Ahora se pueden dar 3 casos, que hayamos obtenido respuesta, que obtengamos un error o que todo se haya obtenido correctamente.
        if not respuesta:
            #Si no tenemos respuesta, no podemos parsear el json, devolvemos error del servidor por pantalla
            return "Error de conexion al servidor."

        if 'error' in respuesta:
            return "No se ha podido encontrar la transacción en la red seleccionada."      

        #data = json.loads(respuesta)
        return respuesta

        
    except bitcoinlib.encoding.EncodingError as e:
        return "La dirección no tiene un formato correcto."
    


def addressHistory(user_id,tx):
    #Mirar cómo queremos los campos en el bot de Telegram
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual

    jsonQuery = getFulcrumQuery('getHistory',tx)
    servidor = get_credentials(redActual)

    try:
        respuesta = consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery)
        #A veces el servidor no responde correctamente, esto no suele pasar pero lo reintentamos
        if not respuesta:     
            for i in range(3):
                respuesta = consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery)
                if respuesta:
                    break
                else:
                    sleep(1)
        
        #Ahora se pueden dar 3 casos, que hayamos obtenido respuesta, que obtengamos un error o que todo se haya obtenido correctamente.
        if not respuesta:
            #Si no tenemos respuesta, no podemos parsear el json, devolvemos error del servidor por pantalla
            return "Error de conexion al servidor."

        if 'error' in respuesta:
            return "No se ha podido encontrar la cuenta seleccionada."      

        data = json.loads(respuesta)
        return data

        
    except bitcoinlib.encoding.EncodingError as e:
        return "La dirección no tiene un formato correcto."
    except json.decoder.JSONDecodeError as e2:
        return "La cantidad de transacciones de esta dirección es superior a la soportada por el programa."
        
