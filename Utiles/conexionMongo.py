#Imports propios
from pymongo import MongoClient
from credentials import get_credentials
#Para funciones exclusivas de mongo que no requieren de los nodos

def register_user(user_id):

    credentials = get_credentials('mongo')
    client = MongoClient(credentials["client"])
    db = client[credentials["db"]]
    collection = db[credentials["collection"]]

    user = collection.find_one({"_id": str(user_id)})
    
    if user: #Usuario encontrado.
        client.close()
        return f"Bienvenido de nuevo! Usa /help para ver más comandos"
    else:
        # Si no está registrado, insertar el nuevo usuario
        new_user = {
            "_id": str(user_id),
            "boolean_field": False,
            "list_mainnet": [],
            "list_testnet": []
        }
        collection.insert_one(new_user)
        client.close()
        return f"Bienvenido, usa /help para ver más comandos !"


def changeNet(user_id):
    credentials = get_credentials('mongo')
    client = MongoClient(credentials["client"])
    db = client[credentials["db"]]
    collection = db[credentials["collection"]]

    user = collection.find_one({"_id": str(user_id)})

    if user:
        #True para testnet false para mainnet
        testnet = user.get("boolean_field", None)
        if testnet is not None:
            testnet = bool(testnet)
        else:
            testnet = False

        result = collection.update_one(
            {"_id": str(user_id)},
            {"$set": {"boolean_field": (not testnet)}}
        )
        client.close()
        return "Se ha cambiado la red"
    else:
        client.close()
        return "Para usar la aplicacion registrate antes usando /start."
    
def booleanFromUser(user_id):
    credentials = get_credentials('mongo')
    client = MongoClient(credentials["client"])
    db = client[credentials["db"]]
    collection = db[credentials["collection"]]

    user = collection.find_one({"_id": str(user_id)})
    client.close()
    
    if user:
        testnet = user.get("boolean_field", None)
        if testnet is not None:
            testnet = bool(testnet)
            return testnet
        else:
            return "Error"