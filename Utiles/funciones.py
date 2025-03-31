import requests
import re
from bitcoinrpc.authproxy import AuthServiceProxy
from pymongo import MongoClient
from datetime import datetime
#Imports propios
from conexionMongo import booleanFromUser
from credentials import *

##########################################################
def isValidBTCAddress(address):
    regex = r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{24,59}$"
    return bool(re.match(regex, address))
##########################################################
def precio_bitcoin():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return str(data['bitcoin']['usd'])
##########################################################
def precioPorBTC(num):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()

    valorEnDols = (data['bitcoin']['usd'])*num
    precio = "{:.2f}".format(valorEnDols)

    return str(precio)+ '$'

##########################################################
def infoBlockchain(user_id):
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual

    if redActual: 
        client = AuthServiceProxy(getTestnetClient())
    else:
        client = AuthServiceProxy(getMainnetClient())

    try: 
        jsonToParse = client.getblockchaininfo()
    except: 
        return "Error de conexión"  
     
    resultadoRed = jsonToParse.get("chain", "Desconocido") 
    
    if resultadoRed == "main":
        redInfo = "mainnet"
    elif resultadoRed == "test":
        redInfo = "testnet"
    else:
        return "Problema con la red."

    fecha_hora = datetime.utcfromtimestamp(jsonToParse["time"])

    bytesEnGB = 1024*1024*1024
    

    retorno = "Información actual sobre la red:\nRed actual: " + redInfo + "\nNúmero de bloques: " + str(jsonToParse["blocks"]) + "\nDificultad actual de la red: " + str(jsonToParse["difficulty"]) + "\
    \nHora UTC registrada: " +  str(fecha_hora) + "\nEspacio en disco: " + str(jsonToParse["size_on_disk"]/bytesEnGB) + " GB."
    
    return retorno
##########################################################
def textoMultisig(dirsConvencionales,dirsMultisig):
    textoRetorno = ""
    if len(dirsConvencionales) != 0:
        textoRetorno = "Direcciones no multisig:\n"
        for i in range(0, len(dirsConvencionales), 2):
            textoRetorno += dirsConvencionales[i] + " ha recibido: " + str(dirsConvencionales[i+1]) + "\n"

    #Direcciones multisig:
    textoRetorno = "Direcciones multisig:\n"
    for i in range(0, len(dirsMultisig), 2):
        multiSigActual = dirsMultisig[i].split()
        textoRetorno += f"La una multisig {multiSigActual[0]}/{multiSigActual[len(multiSigActual)-2]} ha recibido: {str(dirsMultisig[i+1])}\n"
        textoRetorno += "Y está compuesta por las siguientes claves públicas:\n"
        for j in range(1, len(multiSigActual)-2, 1):
            textoRetorno += multiSigActual[j] + "\n"

    return textoRetorno
##########################################################
def check_multisig(transaction):
    for output in transaction['vout']:
        script_asm = output['scriptPubKey']['asm']
        if 'OP_CHECKMULTISIG' in script_asm:
            return True
    return False
##########################################################
def printInputsFromList(list):
    retorno = ""
    for address in list:
        retorno += f"{address}\n"
    return retorno
##########################################################
def outputFormat(list):
    retorno = ""
    for salida in list:
        retorno += f"Dirección: {salida[0]} recibió: {salida[1]} BTC\n"
    return retorno
##########################################################
def infoTx(user_id,tx):
    #1 entrada 1 salida:             tx=c9435711f75903656f0b04d84b4058f2755403aa279774de212f75797c04474f
    #1 entrada varias salidas:       tx=973eaa563475eaa3291612811c0348b260823a4b790f03eaa1a5ae52fa717804
    #varias entradas varias salidas: tx=7274c3d4a3dd41806fa2f56bcccee5495b61d24f796fed3024502d6f231f7c73
    #Multisig salida:                tx=d63667e49701df10b51dfe347e6ed6f59a73f4ef3c883ad9cfee3d23064372a6
    redActual = booleanFromUser(user_id)

    if redActual == "Error":
        return redActual

    if redActual: 
        client = AuthServiceProxy(getTestnetClient())
    else:
        client = AuthServiceProxy(getMainnetClient())
    
    jsonTx = client.getrawtransaction(tx, True)

    # Obtener los inputs
    dirsEntrada = []
    for vin in jsonTx["vin"]:
        prev_tx = client.getrawtransaction(vin["txid"], True)
        if check_multisig(prev_tx):                                                                 #HAY QUE VER SI ESTO HACE FALTA
            return "No hay soporte para las transacciones que toman una multisig de entrada."       #
        vout = prev_tx["vout"][vin["vout"]]
        dirsEntrada.append(vout["scriptPubKey"]["address"])

    if not check_multisig(jsonTx): #En caso de que sea una transacción sin salida multisig procesamos aqui
        dirsSalidaSaldo = [(vout['scriptPubKey']['address'], float(vout['value'])) for vout in jsonTx['vout']]
        suma_total = sum(valor for _, valor in dirsSalidaSaldo)
        return f"La transacción con id: {tx}\ntiene un valor total de: {suma_total} BTC, valorado en: {precioPorBTC(suma_total)} actualmente.\nHa sido enviada por las siguientes direccion/es:\n{printInputsFromList(dirsEntrada)}y la/s salida/s son:\n{outputFormat(dirsSalidaSaldo)}"

    else:#Tratar el procesamiento de la multisig
        dirsConvencionales = []
        dirsMultisig = []
        salidas = []
        suma_total = 0
        #Direcciones normales
        for output in jsonTx.get('vout', []):
            address = output.get('scriptPubKey', {}).get('address')
            if address:
                dirsConvencionales.append(address)
                dirsConvencionales.append(output.get('value'))        #<addr1> <value1> <addr2> <value2> ... <addrn> <valuen>
                suma_total += output.get('value')

        #Multisig
        for output in jsonTx['vout']:
            script_asm = output['scriptPubKey']['asm']
            if 'OP_CHECKMULTISIG' in script_asm:
                dirsMultisig.append(script_asm)
                dirsMultisig.append(output.get('value'))
                suma_total += output.get('value')

        return f"La transacción con id: {tx}\ntiene un valor total de: {suma_total} BTC, valorado en: {precioPorBTC(suma_total)} actualmente.\nHa sido enviada por las siguientes direccion/es:\n{printInputsFromList(dirsEntrada)}Y la/s salida/s se estructuran de la siguiente manera:\n" + textoMultisig(dirsConvencionales,dirsMultisig)
##########################################################
