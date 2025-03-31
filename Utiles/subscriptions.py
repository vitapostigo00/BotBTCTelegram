import asyncio
from pymongo import MongoClient
import zmq
from ApiToken import returnApiToken
from consultasFulcrum import getBalanceNode
from telegram import Bot
from credentials import get_credentials
from ApiToken import ipLocal

async def pushMessage(mensaje, listaUsuarios,bot):
    for usuario in listaUsuarios:
        await bot.send_message(chat_id=usuario, text=mensaje)

async def on_new_block(bot):
    #print("Nuevo bloque detectado:",
    #Hacer barrido para notificar a las cuentas
    #Mirar los fallos de importar la colección que no es...
    credentials = get_credentials('mongo')
    client = MongoClient(credentials["client"])
    db = client[credentials["db"]]
    #Hardcodeamos, si hay tiempo se ajustará get_credentials para los 2 tipos de mongo...
    collection = db["direcciones"]

    cuentas_mainnet = list(collection.find({"testnet": False}))
    #El usuario con id 0 (str(0)) es un usuario que siempre está en mainnet
    for cuenta in cuentas_mainnet:
        balanceDatabase = float(cuenta["last_balance"])
        print("Dirección: " + cuenta["address"])
        actualBalance = getBalanceNode(str(0),cuenta["address"])
        if balanceDatabase != actualBalance:
            if balanceDatabase > actualBalance:
                mensaje = "Mainnet:\nEl saldo de la cuenta: " + cuenta["address"] + " ha decrementado de: " + str(balanceDatabase) + "\
                a: " + str(actualBalance) + "\nLo que representa una diferencia de: " + str(balanceDatabase-actualBalance) + " BTC"
                await pushMessage(mensaje, cuenta["subscribed"],bot)
            elif balanceDatabase < actualBalance:
                mensaje = "Mainnet:\nEl saldo de la cuenta: " + cuenta["address"] + " ha incrementado de: " + str(balanceDatabase) + "\
                a: " + str(actualBalance) + "\nLo que representa un aumento de: " + str(actualBalance - balanceDatabase) + " BTC"
                await pushMessage(mensaje, cuenta["subscribed"],bot)
        #Por último, como ha cambiado el saldo, lo actualizamos en la bbdd:
        collection.update_one(cuenta, {"$set": {"last_balance": actualBalance}})


    """
    #Si vuelve a petar comento de aqui para abajo
    #Esto no es así pero como no tengo configurado los 2 zmqs refresco solo con bloque de mainnet, esto hay que arreglarlo.
    cuentas_testnet = list(collection.find({"testnet": True}))
    #El usuario con id -2 es un usuario que siempre está en testnet
    for cuenta in cuentas_testnet:
        balanceDatabase = float(cuenta["last_balance"])
        actualBalance = getBalanceNode(1,cuenta["address"])
        if balanceDatabase != actualBalance:
            if balanceDatabase > actualBalance:
                mensaje = "Testnet:\nEl saldo de la cuenta: " + cuenta["address"] + " ha decrementado de: " + str(balanceDatabase) + "\
                a: " + str(actualBalance) + "\nLo que representa una diferencia de: " + str(balanceDatabase-actualBalance) + " BTC"
                await pushMessage(mensaje, cuenta["subscribed"],bot)
            elif balanceDatabase < actualBalance:
                mensaje = "Testnet:\nEl saldo de la cuenta: " + cuenta["address"] + " ha incrementado de: " + str(balanceDatabase) + "\
                a: " + str(actualBalance) + "\nLo que representa un aumento de: " + str(actualBalance - balanceDatabase) + " BTC"
                await pushMessage(mensaje, cuenta["subscribed"],bot)
        #Por último, como ha cambiado el saldo, lo actualizamos en la bbdd:
        collection.update_one(cuenta, {"$set": {"last_balance": actualBalance}})
    """

#Reajustar credenciales para local...
async def listen_to_zmq():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp:/"+ ipLocal +"/:8433")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    bot = Bot(token=returnApiToken())

    print("Escuchando el socket...")
    while True:
        topic = socket.recv()
        block_data = socket.recv()
        print("Evento recibido.")
        #print("EVENTO RECIBIDO: " + str(topic))
        #print("BlockData:\n"+str(block_data))
        await on_new_block(bot)
        


async def main():
    await listen_to_zmq()

if __name__ == '__main__':
    asyncio.run(main())


