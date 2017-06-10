#!/bin/env python

import logging
import yaml
from urllib.request import urlopen
from io import BytesIO
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
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
    ##bot.send_message(chat_id=update.message.chat_id, text=update.message.first_name)

def meteo(bot, update):
    """ meteo (callback function    )
    """
    day = 0
    msg = update.message
    tkn = msg.text.split()
    if len(tkn) > 1:
        ville = tkn[1].lower()
        try:
            day = min(int(tkn[2]), 5)
        except (ValueError, TypeError, IndexError):
            day = 0
    else:
        bot.send_message(chat_id=msg.chat_id, text='merci de donner un nom de ville connu')
        return()
    if ville in CONF['villes']:
        url = f"http://www.prevision-meteo.ch/uploads/widget/{ville}_{day}.png"
        ## bot.send_photo(chat_id=msg.chat_id, photo=url)
        img_meteo = BytesIO(urlopen(url).read())
        img_meteo.name = 'img_meteo.jpeg'
        img_meteo.seek(0)
        bot.send_photo(chat_id=msg.chat_id, photo=img_meteo)
    else:
        bot.send_message(chat_id=msg.chat_id, text='ville inconnue')

def usage(bot, update):
    """ help (callback function)
    """
    usage = """
    Comment utiliser le Bot:
    
    /villes
    donne la liste de villes pour lesquelles peut vous donner la météo

    /meteo <ville>
    donne la météo dans <ville> pour la journée

    /meteo <ville> <jour>
    donne la météo dans <ville> pour dans <jour> jours,
    exemple : /meteo lausanne 1

    """
    bot.send_message(chat_id=update.message.chat_id, text=usage)

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
    dispatcher.add_handler(CommandHandler('meteo', meteo))
    dispatcher.add_handler(CommandHandler('météo', meteo))

    ## register the villes / cities command
    dispatcher.add_handler(CommandHandler('villes', cities))
    dispatcher.add_handler(CommandHandler('cities', cities))

    ## register the help / aide command
    dispatcher.add_handler(CommandHandler('usage', usage))
    dispatcher.add_handler(CommandHandler('aide', usage))
    dispatcher.add_handler(CommandHandler('help', usage))

    # now we are in
    updater.start_polling()

__main__()
