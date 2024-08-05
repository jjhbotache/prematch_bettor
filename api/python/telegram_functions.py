import telebot
import threading
import time
import os

# Define el token del bot
TOKEN = os.environ["TELEGRAM_TOKEN_API"]

# Crea una instancia del bot
bot = telebot.TeleBot(TOKEN)

# Lista global de suscriptores
subscribers = set()

# Define el comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, '¡Hola! Soy tu bot de Telegram. Puedes suscribirte usando /subscribe.')

# Define el comando /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, '¡Ayuda! Puedes suscribirte usando /subscribe y desuscribirte usando /unsubscribe.')

# Define el comando /subscribe
@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    chat_id = message.chat.id
    if chat_id not in subscribers:
        subscribers.add(chat_id)
        bot.reply_to(message, '¡Te has suscrito correctamente!\nTe avisaré cuando encuentre una surebet.\nUsa /unsubscribe para desuscribirte.')
    else:
        bot.reply_to(message, '¡Ya estás suscrito!')

# Define el comando /unsubscribe
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    chat_id = message.chat.id
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        bot.reply_to(message, 'Te has desuscrito correctamente.')
    else:
        bot.reply_to(message, 'No estás suscrito.')

# Define una función para manejar mensajes de texto
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, 'Hola, usa /subscribe para avisarte cuando encuentre una surebet!')



# Función para enviar mensajes a los suscriptores
def broadcast_msg(msg):
  for chat_id in subscribers:
    bot.send_message(chat_id, msg)



def main():
  print("Starting bot")
  bot.polling(none_stop=True)
  

threading.Thread(target=main).start()