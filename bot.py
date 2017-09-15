import logging
import settings
import ephem
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters



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

def count(bot,update,args):
    string_args = "_".join(args)
    if string_args.startswith("\"") and string_args.endswith("\""):
        if len(string_args) > 2:
            number = str(len(args)) +' '+ 'word'
            update.message.reply_text(number)
        else: 
            update.message.reply_text('Вы не ввели сообщение')   
    else:
        update.message.reply_text('Введите сообщение в кавычках')

def calc(bot,update,args):
    string_args = "".join(args)
    string_args = string_args.replace("=", "")
    x1=string_args.find("+")
    x2=string_args.find("-")
    x3=string_args.find("*")
    x4=string_args.find("/")

    if x1 != -1:
        parts = string_args.split("+")
        rezult=int(parts[0])+int(parts[1])
    elif x2 != -1:
        parts = string_args.split("-")
        rezult=int(parts[0])-int(parts[1])
    elif x3 != -1:
        parts = string_args.split("*")
        rezult=int(parts[0])*int(parts[1])
    elif x4 != -1:
        parts = string_args.split("/")
        try:
            rezult=int(parts[0])/int(parts[1])
        except ZeroDivisionError:
            rezult = "Деление на ноль"

    update.message.reply_text(rezult)

def word_calc(bot,update,args):
    string_args=""
    word={"один":"1","два":"2", "три":"3","четыре":"4","плюс":"+","минус":"-"}
    i=0
    while i<len(args):
        if args[i] in word:
                string_args+=word.get(args[i])
        i+=1
    calc(bot,update,string_args)


    

def chat(bot, update):
    text_message = update.message.text
    update.message.reply_text(text_message)
    logging.info(text_message)
    

def main():
    updtr = Updater(settings.TELEGRAM_API_KEY)
    
    updtr.dispatcher.add_handler(CommandHandler("start", start_bot))

    updtr.dispatcher.add_handler(CommandHandler("planet", name_of_planet_bot, pass_args = True))
    updtr.dispatcher.add_handler(CommandHandler("wordcount", count, pass_args = True))
    updtr.dispatcher.add_handler(CommandHandler("calc", calc, pass_args = True))
    updtr.dispatcher.add_handler(CommandHandler("word_calc", word_calc, pass_args = True))

    updtr.dispatcher.add_handler(MessageHandler(Filters.text, chat))
    
    updtr.start_polling()
    updtr.idle()

if __name__ == '__main__':
    logging.info('Bot started')
    main()
