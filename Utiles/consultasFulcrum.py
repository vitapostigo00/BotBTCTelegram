import socket
from time import sleep
import json
import bitcoinlib
from funciones import precioPorBTC
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

def consultaFulcrumPesada(host, port, content):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(json.dumps(content).encode('utf-8')+b'\n')
    sleep(0.5)
    sock.shutdown(socket.SHUT_WR)
    res = ""
    while True:
        data = sock.recv(65536)
        if (not data):
            break
        res += data.decode()
    sock.close()
    return res

def checkValidAddr(user_id,address):
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return False

    #Probamos getBalance como función para probar que no haya fallo.
    jsonQuery = getFulcrumQuery('getBalance',address,redActual)
    servidor = get_credentials(redActual)

    try:
        data = json.loads(consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery))
        return True
    
    except bitcoinlib.encoding.EncodingError as e:
        return False
    
    #Los casos están separados por debug...
    except Exception as e2:
        return False

    
def getBalanceNode(user_id,address):
    satsInBTC = 100000000
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual

    jsonQuery = getFulcrumQuery('getBalance',address,redActual)
    servidor = get_credentials(redActual)

    try:
        data = json.loads(consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery))
        confirmed = float(data['result']['confirmed'])
        return confirmed/satsInBTC
    
    except bitcoinlib.encoding.EncodingError as e:
        return "La dirección no tiene un formato correcto."
    

def firstUse(user_id,addr):
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual

    jsonQuery = getFulcrumQuery('firstUse',addr,redActual)
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
            return "Error, no se ha podido encontrar la dirección en la red seleccionada."      

        data = json.loads(respuesta)
        return data

        
    except bitcoinlib.encoding.EncodingError as e:
        return "Error, la dirección no tiene un formato correcto."
    


def addressHistory(user_id,tx):#En desuso porque no es de Teclado.
    
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual

    jsonQuery = getFulcrumQuery('getHistory',tx,redActual)
    servidor = get_credentials(redActual)

    try:
        respuesta = consultaFulcrum(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery)
        #A veces el servidor no responde correctamente, si esto pasa ponemos la función de hacer una consulta más pesada a ver si eso soluciona y lo reintentamos.
        if not respuesta:     
            for i in range(3):
                respuesta = consultaFulcrumPesada(servidor["fulcrum"]["host"],servidor["fulcrum"]["port"], jsonQuery)
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
    

def getBlockFromTx(user_id,tx):
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual

    jsonQuery = getFulcrumQuery('getBlockHash',tx,redActual)
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
    
def parsearTransacciones(historico):
    numTx = len(historico["result"])
    retorno = ""

    if(numTx >5):#Si hay más de 5, devolvemos las últimas 5
        txAProcesar = historico["result"][-5:]
    else:
        txAProcesar = historico["result"]
    for tx in txAProcesar:
        #Mirar altura del bloque, por ahora se quita pero es interesante para conocer el tiempo de uso.
        #retorno += f"Transacción con hash: {tx['tx_hash']} en el bloque: {tx['height']}\n"
        retorno += f"Transacción con hash: {tx['tx_hash']}\n"
    return retorno


def infoCuenta(user_id,address):
    try:
        saldoActual = getBalanceNode(user_id,address)
    except Exception:
        return "Dirección no válida, asegurese de que el formato es correcto"

    if saldoActual=="La dirección no tiene un formato correcto.":
        return saldoActual
    
    retorno = f"La cuenta: {address} tiene actualmente: {saldoActual} BTC por valor de: {precioPorBTC(saldoActual)}\n"

    primerUso = firstUse(user_id,address)

    if isinstance(primerUso,str):
        return primerUso

    retorno += f"Fue usada por primera vez en el bloque número: {primerUso['result']['block_height']}\nCon hash:{primerUso['result']['block_hash']}\nEn la transacción:{primerUso['result']['tx_hash']}\n"

    historicoDirecciones = addressHistory(user_id,address)

    if isinstance(historicoDirecciones,str):#Si es un string indica código de error, simplemente devolvemos lo que tenemos.
        return retorno

    num_entradas = len(historicoDirecciones["result"])

    retorno += f"Se han podido obtener: {num_entradas} direcciones asociadas a la cuenta\n"

    retorno += parsearTransacciones(historicoDirecciones)

    return retorno