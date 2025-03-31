import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from consultasFulcrum import firstUse, getBalanceNode
from funciones import *
from conexionMongo import *
from ApiToken import returnApiToken

nest_asyncio.apply()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(register_user(update.message.from_user.id))


async def help(update: Update, context: CallbackContext) -> None:
    options = ('Los comandos disponibles actualmente son:\n'
    '/blockchaininfo Devuelve información de la red a la que está conectada el bot\n'
    '/precio : Devuelve el precio actual de 1 BTC\n'
    '/cambiarRed Para cambiar entre mainnet y testnet\n'
    '/consultarSaldo para ver el balance de una dirección\n'
    '/consultarTransaccion para obtener información sobre una transacción\n'
    '/primerUso para consultar cuándo fue la primera vez que una dirección recibió fondos\n'
    '/suscribirse para recibir notificaciones en tiempo real de cambios en el saldo de la cuenta que quiera\n'
    '/cancelarSuscripcion para dejar de recibir las notificaciones de suscribirse\n'
    '/mostrarSeguimiento para ver las direcciones que están siendo vigiladas \n'
    )
    await update.message.reply_text(options)


async def blockchainInfo(update: Update, context: CallbackContext) -> None:
        await update.message.reply_text(infoBlockchain(update.message.from_user.id))

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
                await update.message.reply_text(str(balance))
        else:
            await update.message.reply_text('La dirección proporcionada no es válida')

    else:
        await update.message.reply_text('Por favor, proporciona una dirección de Bitcoin para consultar el saldo.')

async def consultarTx(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        tx = context.args[0]
        await update.message.reply_text(infoTx(update.message.from_user.id,tx))
    else:
        await update.message.reply_text('Por favor, escribe una transaccion junto al comando para obtener información sobre ella.')

async def primerUso(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        address = context.args[0]
        await update.message.reply_text(firstUse(update.message.from_user.id,address))
    else:
        await update.message.reply_text('Por favor, escribe una transaccion junto al comando para obtener información sobre ella.')

async def suscribirse(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        address = context.args[0]
        await update.message.reply_text(subscribeUserToAddress(update.message.from_user.id,address))
    else:
        await update.message.reply_text('Por favor, escribe una dirección junto al comando para ser notificado de cambios en el saldo.')

async def cancelarSuscripcion(update: Update, context: CallbackContext) -> None:
    if len(context.args) > 0:
        address = context.args[0]
        await update.message.reply_text(unsubscribeUserToAddress(update.message.from_user.id,address))
    else:
        await update.message.reply_text('Por favor, escribe una dirección junto al comando para no ser notificado.')

async def mostrarSeguimiento(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(showFollowing(update.message.from_user.id))

async def main():

    app = Application.builder().token(returnApiToken ()).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("blockchainInfo", blockchainInfo))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("cambiarRed", cambiarRed))
    app.add_handler(CommandHandler("consultarSaldo", consultarSaldo))
    app.add_handler(CommandHandler("consultarTransaccion", consultarTx))
    app.add_handler(CommandHandler("primerUso", primerUso))
    app.add_handler(CommandHandler("suscribirse", suscribirse))
    app.add_handler(CommandHandler("cancelarSuscripcion", cancelarSuscripcion))
    app.add_handler(CommandHandler("mostrarSeguimiento", mostrarSeguimiento))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())