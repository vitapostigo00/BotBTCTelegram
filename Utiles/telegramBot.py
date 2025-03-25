import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from consultasFulcrum import getBalanceNode
from funciones import *
from conexionMongo import *
from ApiToken import returnApiToken

nest_asyncio.apply()

TOKEN = returnApiToken ()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(register_user(update.message.from_user.id))


async def help(update: Update, context: CallbackContext) -> None:
    options = ('Los comandos disponibles actualmente son:\n'
    '/blockchaininfo Devuelve información de la red a la que está conectada el bot\n'
    '/precio : Devuelve el precio actual de 1 BTC\n'
    '/cambiarRed Para cambiar entre mainnet y testnet\n'
    '/consultarSaldo para ver el balance de una dirección'
    )
    await update.message.reply_text(options)


async def blockchaininfo(update: Update, context: CallbackContext) -> None:
    blockchain = infoBlockchain(update.message.from_user.id)
    if update.message:
        await update.message.reply_text(f'Estás en la blockchain: {blockchain}')
    else:
        print("Error: El mensaje no está presente en update.")

async def precio(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('El precio actual de 1 Bitcoin es: ' + precio_bitcoin() + " $")

async def cambiarRed(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('' + changeNet(update.message.from_user.id))

async def consultarSaldo(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        address = context.args[0]
        if isValidBTCAddress(address):
            balance = getBalanceNode(update.message.from_user.id,address)
            if isinstance(balance, float):
                await update.message.reply_text(f'El saldo asociado a la dirección {address} es: {balance} BTC con un valor actual de: ' + precioPorBTC(balance))
            else:
                #Cuando la dirección está mal directamente se guarda en balance para ser imprimido
                await update.message.reply_text(balance)
            
        else:
            await update.message.reply_text('La dirección proporcionada no es válida')

    else:
        await update.message.reply_text('Por favor, proporciona una dirección de Bitcoin para consultar el saldo.')


async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("blockchaininfo", blockchaininfo))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("cambiarRed", cambiarRed))
    app.add_handler(CommandHandler("consultarSaldo", consultarSaldo))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())