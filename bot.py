import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
import ephem
import datetime

logging.basicConfig() 


def start_bot(bot, update):
    mytext = """Привет, {}{}
Я простой бот и понимаю только команду /start
    """.format(update.message.chat.first_name,update.message.chat.last_name)
    logging.info('Пользователь {} нажал /start'.format(update.message.chat.username))
    update.message.reply_text(mytext)

def name_of_planet_bot(bot, update, args):
    text = args[0]
    planets = getattr(ephem, text, None)
    if not planets:
        update.message.reply_text('Извини, такой планеты нет')
        return 
    answer = ephem.constellation(planets(datetime.datetime.now()))
    update.message.reply_text(answer)



def chat(bot, update):

    logging.info(text)
    

def main():
    updtr = Updater(settings.TELEGRAM_API_KEY)
    
    updtr.dispatcher.add_handler(CommandHandler("start", start_bot))

    updtr.dispatcher.add_handler(CommandHandler("planet", name_of_planet_bot, pass_args = True))
    updtr.dispatcher.add_handler(MessageHandler(Filters.text, chat))
    
    updtr.start_polling()
    updtr.idle()

if __name__ == "__main__":
    logging.info('Bot started')
    main()
