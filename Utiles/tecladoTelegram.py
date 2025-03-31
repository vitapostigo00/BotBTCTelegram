from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
from conexionMongo import booleanFromUser
from funciones import infoTx

#########################################################################
async def keyboard_principal(update: Update, context: CallbackContext) -> None:
    
    red = booleanFromUser(update.message.from_user.id)
    red = "Testnet3" if red else "Mainnet"

    keyboard = [
        [f"Red actual: {red}"],
        ["Consultas Blockchain"],
        ["Seguimiento de direcciones"],
        ["Precio"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Selecciona una opción:", reply_markup=reply_markup)

    # Resetear estado de espera si el usuario vuelve al inicio
    context.user_data.pop("esperando_datos", None)

#########################################################################
async def keyboard_consultas(update: Update, context: CallbackContext) -> None:
    keyboard = [
        ["Estado de la Blockchain"],
        ["Cuenta"],
        ["Transacción"],
        ["Bloque"],
        ["Volver al inicio"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Selecciona una opción:", reply_markup=reply_markup)

#########################################################################
async def keyboard_seguimiento(update: Update, context: CallbackContext) -> None:
    keyboard = [
        ["Seguir dirección"],
        ["Dejar de seguir dirección"],
        ["Cuentas en seguimiento"],
        ["Volver al inicio"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Selecciona una opción:", reply_markup=reply_markup)

#########################################################################
async def handle_response_keyboard(update: Update, context: CallbackContext) -> None:
######################TOMA  DATOS######################
    text = update.message.text
    # Comprobación si el bot está esperando datos
    if "esperando_datos" in context.user_data:
        tipo_dato = context.user_data["esperando_datos"]
        user_id = update.message.from_user.id

        if tipo_dato == "transaccion":
            respuesta = infoTx(user_id, text)
            await update.message.reply_text(respuesta)
            await keyboard_consultas(update, context)

        elif tipo_dato == "bloque":
            from funciones import blockInfo
            respuesta = blockInfo(user_id, text)
            await update.message.reply_text(respuesta)
            await keyboard_consultas(update, context)

        elif tipo_dato == "cuenta":
            from consultasFulcrum import infoCuenta
            respuesta = infoCuenta(user_id, text)
            await update.message.reply_text(respuesta)
            await keyboard_consultas(update, context)

        elif tipo_dato == "seguir_direccion":
            from conexionMongo import subscribeUserToAddress
            respuesta = subscribeUserToAddress(user_id, text)
            await update.message.reply_text(respuesta)
            await keyboard_seguimiento(update, context)

        elif tipo_dato == "dejar_seguir_direccion":
            from conexionMongo import unsubscribeUserToAddress
            respuesta = unsubscribeUserToAddress(user_id, text)
            await update.message.reply_text(respuesta)
            await keyboard_seguimiento(update, context)

        context.user_data.pop("esperando_datos")
######################TOMA  DATOS######################
######################CASO INICIO######################
    red = booleanFromUser(update.message.from_user.id)
    red = "Testnet3" if red else "Mainnet"

    if text == f"Red actual: {red}":
        from conexionMongo import changeNet
        changeNet(update.message.from_user.id)
        red = booleanFromUser(update.message.from_user.id)
        red = "Testnet3" if red else "Mainnet"
        await update.message.reply_text(f"Se ha cambiado la red a: {red}")
        await keyboard_principal(update, context)

    elif text == "Consultas Blockchain":
        await keyboard_consultas(update, context)

    elif text == "Seguimiento de direcciones":
        await keyboard_seguimiento(update, context)

    elif text == "Precio":
        from telegramBot import precio
        await precio(update, context)
        await keyboard_principal(update, context)
######################CASO INICIO######################
#####################CASO CONSULTAS####################
    elif text == "Estado de la Blockchain":
        from telegramBot import blockchainInfo
        await blockchainInfo(update, context)
        await keyboard_consultas(update, context)

    elif text == "Cuenta":
        await update.message.reply_text("Por favor, escribe la dirección de la cuenta:")
        context.user_data["esperando_datos"] = "cuenta"

    elif text == "Transacción":
        await update.message.reply_text("Por favor, escribe el id de la transacción:")
        context.user_data["esperando_datos"] = "transaccion"

    elif text == "Bloque":
        await update.message.reply_text("Por favor, escribe el hash, número de bloque o transacción para dar datos del bloque que la contiene:")
        context.user_data["esperando_datos"] = "bloque"

    elif text == "Volver al inicio":
        await keyboard_principal(update, context)
#####################CASO CONSULTAS####################
####################CASO SEGUIMIENTO###################
    elif text == "Seguir dirección":
        await update.message.reply_text("Por favor, escribe la dirección que quieres seguir:")
        context.user_data["esperando_datos"] = "seguir_direccion"

    elif text == "Dejar de seguir dirección":
        await update.message.reply_text("Por favor, escribe la dirección que quieres dejar de seguir:")
        context.user_data["esperando_datos"] = "dejar_seguir_direccion"

    elif text == "Cuentas en seguimiento":
        from telegramBot import mostrarSeguimiento
        await mostrarSeguimiento(update, context)
        await keyboard_seguimiento(update, context)

    else:
        pass
####################CASO SEGUIMIENTO###################
#########################################################################
