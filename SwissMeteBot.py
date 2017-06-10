#!/bin/env python

import logging
import yaml
from telegram.ext import Updater
from telegram.ext import CommandHandler

# read config file
with open("config.yml", 'r') as ymlfile:
    CONF = yaml.load(ymlfile)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(bot, update):
    """ Start (callback funtion)
    Args:   bot, the bot
            update, update message
    Return: -
    """
    print(update)
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
    ##bot.send_message(chat_id=update.message.chat_id, text=update.message.first_name)

def meteo(bot, update):
    """ meteo (callback function    )
    """
    print("meteo called", update)
    msg = update.message
    tkn = msg.text.split()
    print(tkn)
    if len(tkn) > 1:
        ville = tkn[1]
        print(ville)
    else:
        bot.send_message(chat_id=msg.chat_id, text='merci de donner la ville considérée')
        return()
    if ville in CONF['villes']:
        bot.send_message(chat_id=msg.chat_id,
                         text=f"http://www.prevision-meteo.ch/uploads/widget/{ville}_0.png")
    else:
        bot.send_message(chat_id=msg.chat_id, text='ville inconnue')


def cities(bot, update):
    """ cities (callback function)
    """
    txt = "Les villes connues à ce jour par le bot:\n"
    for ville in CONF['villes']:
        txt += f"- {ville}\n"
    bot.send_message(chat_id=update.message.chat_id,
                     text=txt)


def __main__():
    

    updater = Updater(token=CONF['token'])
    dispatcher = updater.dispatcher

    ## register the start command
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    ## register the meteo command
    meteo_handler = CommandHandler('meteo', meteo)
    dispatcher.add_handler(meteo_handler)

    ## register the villes / cities command
    dispatcher.add_handler(CommandHandler('villes', cities))
    dispatcher.add_handler(CommandHandler('cities', cities))


    # now we are in
    updater.start_polling()

__main__()
