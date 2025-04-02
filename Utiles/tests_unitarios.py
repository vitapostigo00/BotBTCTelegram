import random
import unittest
from funciones import infoBlockchain, numBloquesRed
from conexionMongo import *
from consultasFulcrum import *

class TestMiModulo(unittest.TestCase):
    ##Realmente hay que probar conexión nodo (funciones) y conexión fulcrum
    def test_conexion_fulcrum(self):
        bloquesMainnet = numBloquesRed(0)
        self.assertIsInstance(bloquesMainnet, int)
        bloquesTestnet = numBloquesRed(1)
        self.assertIsInstance(bloquesTestnet, int)
        

if __name__ == '__main__':
    unittest.main()
