import asyncio
import nest_asyncio
from telegram import Update,BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from consultasFulcrum import firstUse
from funciones import *
from conexionMongo import *
from ApiToken import returnApiToken
from tecladoTelegram import *

nest_asyncio.apply()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(register_user(update.message.from_user.id))


async def help(update: Update, context: CallbackContext) -> None:
    options = (
    'Usa /keyboard para poder interactuar con el teclado con todas las funciones disponibles.\n'
    'De forma alternativa puedes usar los comandos que se muestran a continuación para hacer una serie más reducida de consultas:\n'
    '/blockchaininfo Devuelve información de la red a la que está conectada el bot.\n'
    '/precio Devuelve el precio actual de 1 BTC.\n'
    '/cambiarRed Para cambiar entre mainnet y testnet.\n'
    '/consultarTransaccion Para obtener información sobre una transacción.\n'
    '/suscribirse Para recibir notificaciones en tiempo real de cambios en el saldo de las direcciones deseadas.\n'
    '/cancelarSuscripcion Para dejar de recibir las notificaciones de suscribirse.\n'
    '/mostrarSeguimiento Para ver las direcciones que están siendo vigiladas.\n'
    )
    await update.message.reply_text(options)


async def blockchainInfo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(infoBlockchain(update.message.from_user.id))

async def precio(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('El precio actual de 1 Bitcoin es: ' + precio_bitcoin() + " $")

async def cambiarRed(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('' + changeNet(update.message.from_user.id))

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

    comandos = [
        BotCommand("start", "Iniciar bot"),
        BotCommand("help", "Mostrar comandos"),
        BotCommand("keyboard", "Mostrar teclado"),
    ]

    await app.bot.set_my_commands(comandos)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("blockchainInfo", blockchainInfo))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("cambiarRed", cambiarRed))
    app.add_handler(CommandHandler("consultarTransaccion", consultarTx))
    app.add_handler(CommandHandler("primerUso", primerUso))
    app.add_handler(CommandHandler("suscribirse", suscribirse))
    app.add_handler(CommandHandler("cancelarSuscripcion", cancelarSuscripcion))
    app.add_handler(CommandHandler("mostrarSeguimiento", mostrarSeguimiento))
    
    ##De tecladoTelegram.py
    app.add_handler(CommandHandler("keyboard", keyboard_principal))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response_keyboard))

    await app.run_polling()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())