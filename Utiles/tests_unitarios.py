import random
import unittest
from funciones import infoBlockchain, numBloquesRed
from conexionMongo import *
from consultasFulcrum import *

import json
import requests
import random
from concurrent.futures import ThreadPoolExecutor

# URL para obtener la altura más reciente del bloque
url_tip_height = "https://blockstream.info/api/blocks/tip/height"

# Función para obtener la altura máxima del bloque
def obtener_altura_maxima():
    response = requests.get(url_tip_height)
    if response.status_code == 200:
        return int(response.text)
    else:
        print(f"Error al obtener altura máxima: {response.status_code}")
        return None

# Función para obtener x bloques aleatorios
def obtener_bloques_aleatorios(altura_maxima, cantidad):
    return random.sample(range(altura_maxima), cantidad)

def obtener_hash_bloque(height):
    url_bloque = f"https://blockstream.info/api/block-height/{height}"
    response = requests.get(url_bloque)
    
    print(f"Respuesta para el bloque {height}: {response.text}")
    
    if response.status_code == 200:
        return response.text.strip()
    else:
        print(f"Error al obtener el hash del bloque {height}: {response.status_code}")
        return None

def returnAddresses(data):
    addresses = []
    
    if "vin" in data:
        for vin in data["vin"]:
            if vin.get("prevout") is not None and "scriptpubkey_address" in vin["prevout"]:
                addresses.append(vin["prevout"]["scriptpubkey_address"])

    for vout in data["vout"]:
        if "scriptpubkey_address" in vout:
            addresses.append(vout["scriptpubkey_address"])

    return addresses

# Función para obtener las transacciones de un bloque por su hash
def obtener_transacciones(hash_bloque):
    url_tx = f"https://blockstream.info/api/block/{hash_bloque}/txs/"
    response = requests.get(url_tx)
    
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError as e:
            print(f"Error al parsear JSON para el bloque {hash_bloque}: {e}")
            return None
    else:
        print(f"Error al obtener las transacciones del bloque {hash_bloque}: {response.status_code}")
        return None
    
def devolverBloques(cantidad_bloques):
    altura_maxima = obtener_altura_maxima()
    if not altura_maxima:
        return
    
    bloques_aleatorios = obtener_bloques_aleatorios(altura_maxima, cantidad_bloques)
    print(f"BLOQUES ALEATORIOS: {bloques_aleatorios}")

    all_addresses = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        hashes_bloques = list(executor.map(obtener_hash_bloque, bloques_aleatorios))
        hashes_bloques = [hash_bloque for hash_bloque in hashes_bloques if hash_bloque]

        transacciones_list = list(executor.map(obtener_transacciones, hashes_bloques))

        for transacciones in transacciones_list:
            if transacciones:
                addresses = list(executor.map(returnAddresses, transacciones))
                all_addresses.extend([address for sublist in addresses for address in sublist])

    return all_addresses

class TestMiModulo(unittest.TestCase):
    ##Realmente hay que probar conexión nodo (funciones) y conexión fulcrum
    def test_conexion_fulcrum(self):
        bloquesMainnet = numBloquesRed(0)
        self.assertIsInstance(bloquesMainnet, int)
        bloquesTestnet = numBloquesRed(1)
        self.assertIsInstance(bloquesTestnet, int)
        sumaCuentas = 0
        #Ahora vamos a obtener muchas direcciones y consultar el saldo en el nodo para sumar todos los saldos (solo para ver que getBalance funciona bien)
        #Vamos a intentar sacar los últimos 5 bloques y consultar el saldo de todas ellas a ver si alguna lanza un fallo, puede tardar...
        for direccion in devolverBloques(5):
            sumaCuentas += getBalanceNode(str(0),direccion)

        print(sumaCuentas)


        

if __name__ == '__main__':
    unittest.main()
