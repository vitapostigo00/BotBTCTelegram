import random
import unittest
from funciones import infoBlockchain, numBloquesRed
from conexionMongo import *
from consultasFulcrum import *

class TestMiModulo(unittest.TestCase):
    ##Realmente hay que probar conexión nodo (funciones) y conexión fulcrum
    def test_conexion_fulcrum(self):
        self.assertIsInstance(numBloquesRed(0), int)
        self.assertIsInstance(numBloquesRed(1), int)
        self.assertIsInstance(numBloquesRed(0), int)
        self.assertIsInstance(numBloquesRed(1), int)
        

if __name__ == '__main__':
    unittest.main()
