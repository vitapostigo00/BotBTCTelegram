import random
import unittest
from funciones import infoBlockchain
from conexionMongo import *
from consultasFulcrum import *

class TestMiModulo(unittest.TestCase):

    def test_conexion_mongo(self):
        #Comprobamos que si iniciamos 2 veces, el usuario recibe un mensaje diferente.
        user_id = str(random.randrange(10**8, 10**10))      #Generamos una id de usuario nueva (hará falta borrarla en un futuro).
        self.assertEqual(register_user(user_id), f"Bienvenido, usa /help para ver más comandos !")
        self.assertEqual(register_user(user_id), f"Bienvenido de nuevo! Usa /help para ver más comandos")
        self.assertEqual(booleanFromUser(user_id),False) #Por defecto debe estar en mainnet
        self.assertEqual(changeNet(user_id),"Se ha cambiado la red")
        self.assertEqual(booleanFromUser(user_id),True)
        #Comprobamos que se ha cambiado la red.


    def test_conexion_fulcrum_main(self):
        user_id = str(random.randrange(10**8, 10**10))
        register_user(user_id)
        data = getBlockFromTx(user_id,"973eaa563475eaa3291612811c0348b260823a4b790f03eaa1a5ae52fa717804")
        block_hash = data["result"]["block_hash"]
        block_height = data["result"]["block_height"]
        self.assertEqual(str(block_hash),"00000000000000000000b7674e9e8ea9fc63976f0c625697337a4d7a791e13f1")
        self.assertEqual(str(block_height),"889516")
        #Direccion de Satoshi, como la gente le manda sats continuamente, comprobamos que sea mayor a 102.97 BTC (cantidad a 26/03/25)
        #No obstante, se hace la comparacion con 52.97 ya que los 50BTCs del primer bloque no son gastables y Fulcrum devuelve los UTXOs que se permite gastar una cuenta
        #para su balance
        self.assertGreater(getBalanceNode(user_id,"1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"),52.96)
        #print(firstUse(user_id,"1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"))
        #self.assertEqual()
        
    def test_conexion_fulcrum_test(self):
        user_id = str(random.randrange(10**8, 10**10))
        register_user(user_id)
        self.assertEqual(changeNet(user_id),"Se ha cambiado la red")
        self.assertEqual(booleanFromUser(user_id),True)
        #Nos aseguramos del cambio de ted
        data = getBlockFromTx(user_id,"7ab37665fff5f19e67014c7d50957e53cb2435fb08c654448235c0002c77edb8")
        block_hash = data["result"]["block_hash"]
        block_height = data["result"]["block_height"]
        self.assertEqual(str(block_hash),"00000000055d7963c7f08164e3e2c98eff70cc884575f24c6a5faa48037c3f5f")
        self.assertEqual(str(block_height),"4097391")
        self.assertGreater(getBalanceNode(user_id,"n3GNqMveyvaPvUbH469vDRadqpJMPc84JA"),0.669)

    def test_conexion_nodo_mainnet(self):
        user_id = str(random.randrange(10**8, 10**10))
        register_user(user_id)
        #self.assertEqual(infoBlockchain(user_id),"mainnet")

    def test_conexion_nodo_testnet(self):
        user_id = str(random.randrange(10**8, 10**10))
        register_user(user_id)
        self.assertEqual(changeNet(user_id),"Se ha cambiado la red")
        #self.assertEqual(infoBlockchain(user_id),"testnet")

        
        
        


if __name__ == '__main__':
    unittest.main()
