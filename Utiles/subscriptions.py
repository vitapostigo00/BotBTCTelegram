import asyncio
import signal
from pymongo import MongoClient
import zmq
import threading
from ApiToken import returnApiToken
from consultasFulcrum import getBalanceNode
from telegram import Bot
from credentials import get_credentials
from ApiToken import ipLocal


async def pushMessage(mensaje, listaUsuarios,bot):
    for usuario in listaUsuarios:
        await bot.send_message(chat_id=usuario, text=mensaje)


async def on_new_block(bot):
    #Hacer barrido para notificar a las cuentas
    credentials = get_credentials('mongo')
    client = MongoClient(credentials["client"])
    db = client[credentials["db"]]
    #Hardcodeamos, si hay tiempo se ajustará get_credentials para los 2 tipos de mongo...
    collection = db["direcciones"]

    cuentas_mainnet = list(collection.find({"testnet": False}))
    #El usuario con id 0 (str(0)) es un usuario que siempre está en mainnet
    for cuenta in cuentas_mainnet:
        try:
            balanceDatabase = float(cuenta["last_balance"])
            actualBalance = getBalanceNode(str(0),cuenta["address"])
            if balanceDatabase != actualBalance:
                if balanceDatabase > actualBalance:
                    mensaje = f"Mainnet:\nEl saldo de la cuenta: {cuenta['address']} ha decrementado de: {str(balanceDatabase)} a:  {str(actualBalance)}\nLo que representa una diferencia de: {str(balanceDatabase - actualBalance)} BTC"
                    await pushMessage(mensaje, cuenta["subscribed"],bot)
                elif balanceDatabase < actualBalance:
                    mensaje = f"Mainnet:\nEl saldo de la cuenta: {cuenta['address']} ha incrementado de: {str(balanceDatabase)} a:  {str(actualBalance)}\nLo que representa un aumento de: {str(actualBalance - balanceDatabase)} BTC"
                    await pushMessage(mensaje, cuenta["subscribed"],bot)
                #Por último, como ha cambiado el saldo, lo actualizamos en la bbdd:
                collection.update_one(cuenta, {"$set": {"last_balance": actualBalance}})
        except:
            #Para depurar por consola si tiene algún fallo, es importante que el cliente cierre...
            print(f"Error arrojado por la cuenta: {cuenta['address']}")
        
    client.close()

async def on_new_block_testnet(bot):
    #Hacer barrido para notificar a las cuentas
    credentials = get_credentials('mongo')
    client = MongoClient(credentials["client"])
    db = client[credentials["db"]]
    #Hardcodeamos, si hay tiempo se ajustará get_credentials para los 2 tipos de mongo...
    collection = db["direcciones"]

    cuentas_mainnet = list(collection.find({"testnet": True}))
    #El usuario con id 0 (str(1)) es un usuario que siempre está en testnet
    for cuenta in cuentas_mainnet:
        try:
            balanceDatabase = float(cuenta["last_balance"])
            actualBalance = getBalanceNode(str(1),cuenta["address"])
            if balanceDatabase != actualBalance:
                if balanceDatabase > actualBalance:
                    mensaje = f"Testnet:\nEl saldo de la cuenta: {cuenta['address']} ha decrementado de: {str(balanceDatabase)} a:  {str(actualBalance)}\nLo que representa una diferencia de: {str(balanceDatabase - actualBalance)} BTC"
                    await pushMessage(mensaje, cuenta["subscribed"],bot)
                elif balanceDatabase < actualBalance:
                    mensaje = f"Testnet:\nEl saldo de la cuenta: {cuenta['address']} ha incrementado de: {str(balanceDatabase)} a:  {str(actualBalance)}\nLo que representa un aumento de: {str(actualBalance - balanceDatabase)} BTC"
                    await pushMessage(mensaje, cuenta["subscribed"],bot)
                #Por último, como ha cambiado el saldo, lo actualizamos en la bbdd:
                collection.update_one(cuenta, {"$set": {"last_balance": actualBalance}})
        except:
            #Para depurar por consola si tiene algún fallo, es importante que el cliente cierre...
            print(f"Error arrojado por la cuenta: {cuenta['address']}")
        
    client.close()

async def listen_to_zmq():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://"+ ipLocal() +":8433")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    bot = Bot(token=returnApiToken())

    print("Escuchando el socket 8433")
    while True:
        topic = socket.recv()
        block_data = socket.recv()
        print("Bloque de mainnet.")
        await on_new_block(bot)

async def listen_to_zmq_testnet():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://"+ ipLocal() +":18433")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    bot = Bot(token=returnApiToken())

    print("Escuchando el socket 18433")
    while True:
        topic = socket.recv()
        block_data = socket.recv()
        print("Bloque de testnet.")
        await on_new_block_testnet(bot)
        
def ejecutar_en_thread_1():
    asyncio.run(listen_to_zmq())

def ejecutar_en_thread_2():
    asyncio.run(listen_to_zmq_testnet())

async def main():
    thread1 = threading.Thread(target=ejecutar_en_thread_1)
    thread2 = threading.Thread(target=ejecutar_en_thread_2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


if __name__ == '__main__':
    asyncio.run(main())