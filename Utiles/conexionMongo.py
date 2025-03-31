import re
from pymongo import MongoClient
from credentials import get_credentials
#Para funciones que son principalmente actualizaciones y consultas de la base de datos.

##########################################################
def isValidBTCAddress(address):
    regex = r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{24,59}$"
    return bool(re.match(regex, address))
##########################################################
def createNewAddressEntry(user_id,address):
    from credentials import addr2scripthash
    from consultasFulcrum import getBalanceNode
    boolFromUser =  booleanFromUser(user_id)
    return {
        "address": str(address),
        "testnet": boolFromUser,
        "scriptHash": str(addr2scripthash(address,boolFromUser)),
        "last_balance": str(getBalanceNode(user_id,address)),
        "subscribed": [str(user_id)]
    }
##########################################################
def register_user(user_id):
    credentials = get_credentials('mongo')
    client = MongoClient(credentials["client"])
    db = client[credentials["db"]]
    collection = db[credentials["collection"]]

    user = collection.find_one({"_id": str(user_id)})
    
    if user: #Usuario encontrado.
        client.close()
        return f"Bienvenido de nuevo!\nUsa /help si quieres usar los comando o /keyboard si quieres el teclado para interactuar conmigo."
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
        return f"Bienvenido, usa /help si quieres usar los comando o /keyboard si quieres el teclado para interactuar conmigo."
##########################################################
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
##########################################################
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
##########################################################
#Falta actualizarlo en la colección base.

def subscribeUserToAddress(user_id,address):
    credentials = get_credentials('mongo')
    client = MongoClient(credentials["client"])
    db = client[credentials["db"]]
    collection = db["direcciones"]

    direccion = collection.find_one({"address": str(address)})

    userInTestnet = booleanFromUser(user_id)

    #No debería darse pero puede servir para depurar en caso de que la base de datos sea inconsistente.
    if not isinstance(userInTestnet, bool):
        return "Error en el programa"

    if direccion:
        collection.update_one(
            {"address": str(address)},
            {"$push": {"subscribed": str(user_id)}}
        )
        #Actualizamos en paralelo la cuenta para facilitar el seguimiento de las cuentas que sigue un usuario
        collection = db[credentials["collection"]]
        if userInTestnet:
            collection.update_one(
                {"_id": str(user_id)},
                {"$push": {"list_testnet": str(address)}}
            )
        else:
            collection.update_one(
                {"_id": str(user_id)},
                {"$push": {"list_mainnet": str(address)}}
            )
        client.close()
        return "Se le notificarán los cambios en la dirección: " + str(address)
    
    else:
        if isValidBTCAddress(address):
            try:
                entryToInsert = createNewAddressEntry(user_id,address)
                collection.insert_one(entryToInsert)
                collection = db[credentials["collection"]]
                if userInTestnet:
                    collection.update_one(
                        {"_id": str(user_id)},
                        {"$push": {"list_testnet": str(address)}}
                    )
                else:
                    collection.update_one(
                        {"_id": str(user_id)},
                        {"$push": {"list_mainnet": str(address)}}
                    )
                client.close()
                return "Se le notificarán los cambios en la dirección: " + str(address)
            
            except:
                client.close()
                return "Error con la dirección solicitada"
        else:
            client.close()
            return "La dirección proporcionada no es válida."
##########################################################
def unsubscribeUserToAddress(user_id,address):
    credentials = get_credentials('mongo')
    client = MongoClient(credentials["client"])
    db = client[credentials["db"]]
    collection = db["direcciones"]

    direccion = collection.find_one({"address": str(address)})

    if direccion and str(user_id) in direccion.get("subscribed", []):
        collection.update_one(
            {"address": str(address)},
            {"$pull": {"subscribed": str(user_id)}}
        )
        userInTestnet = booleanFromUser(user_id)

        #No debería darse pero puede servir para depurar en caso de que la base de datos sea inconsistente.
        if not isinstance(userInTestnet, bool):
            return "Error en el programa"
        
        #Si ya no queda nadie vigilando esa dirección la borra.
        collection.find_one_and_delete({"subscribed": {"$size": 0}})
        #Actualizamos en paralelo igual que en subscribe
        collection = db[credentials["collection"]]

        if userInTestnet:
            collection.update_one(
                {"_id": str(user_id)},
                {"$pull": {"list_testnet": str(address)}}
            )
        else:
            collection.update_one(
                {"_id": str(user_id)},
                {"$pull": {"list_mainnet": str(address)}}
            )

        client.close()
        return "Ya no recibirá notifiaciones sobre la dirección: " + str(address)
    
    else:
        return "No está siguiendo esa dirección actualmente, pruebe a revisarla o a cambiar de red."
    

def showFollowing(user_id):
    credentials = get_credentials('mongo')
    client = MongoClient(credentials["client"])
    db = client[credentials["db"]]
    collection = db[credentials["collection"]]

    user = collection.find_one({"_id": str(user_id)})

    if not user["list_mainnet"]:
        texto_mainnet = "No está siguiendo direcciones en mainnet.\n"
    else:
        texto_mainnet = "Está siguiendo las siguientes direcciones en Mainnet:\n"
        for address in user["list_mainnet"]:
            texto_mainnet += str(address) + "\n"

    if not user["list_testnet"]:
        texto_testnet = "No está siguiendo direcciones en testnet.\n"
    else:
        texto_testnet = "Está siguiendo las siguientes direcciones en Testnet:\n"
        for address in user["list_testnet"]:
            texto_testnet += str(address) + "\n"

    texto_mainnet += texto_testnet
    client.close()
    return texto_mainnet