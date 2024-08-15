import telebot
import threading
from dotenv import load_dotenv
import os

# Carga las variables del archivo .env en el entorno
load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN_API')

# Crea una instancia del bot
bot = telebot.TeleBot(TOKEN)

# Ruta del archivo de suscriptores
SUBSCRIBERS_FILE = 'subscribers.txt'

# Carga los suscriptores desde el archivo
def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, 'r') as file:
            subscribers = set(file.read().splitlines())
    except FileNotFoundError:
        subscribers = set()
    return subscribers

# Guarda los suscriptores en el archivo
def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, 'w') as file:
        file.write('\n'.join(subscribers))

# Lista global de suscriptores
subscribers = load_subscribers()

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
        save_subscribers(subscribers)  # Guarda los suscriptores actualizados
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