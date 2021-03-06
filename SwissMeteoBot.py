#!/bin/env python
"""
    Swiss Meteo Bot -- Telegram Bot sharing information about swiss meteo
    Copyright (C) 2017 mfutech (mfutech@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import logging
import re
from io import BytesIO
from urllib.request import urlopen
import yaml
import requests
from lxml import etree

from telegram.ext import Updater
from telegram.ext import CommandHandler

# read config file
with open("config.yml", 'r') as ymlfile:
    CONF = yaml.load(ymlfile)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def possible_cities(search):
    """ possible_cities

    will return list of known cities matching search

    Arg: search : string to search for
    Return: a list of possible cities
    """
    url = 'http://www.prevision-meteo.ch/services'
    values = {
        'widget-localite': search,
        'valider': 'Valider'
    }
    res = requests.post(url, values)
    html_parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(res.content), html_parser)
    opts = tree.xpath('//select[@name="widget-localite2"]/option')
    cities_list = {}
    for opt in opts:
        name = opt.text
        match = re.match(r'(\d+)\s+(.*)(,.*)*', opt.values()[0])
        if match:
            value = re.sub(r'[()]', '', match[2])
            value = (re.sub(r'\s+', '-', value)).lower()
            cities_list[value] = name

    #cities_list = list(map(lambda x: x.values, opts))
    return cities_list


def get_meteo(city, day):
    """ get_meteo

    Arg: city (string) for which we need a meteo images
    Result:
        - False if city does not exists
        - image (BytesIO) if successfull
    """
    url = f"http://www.prevision-meteo.ch/uploads/widget/{city}_{day}.png"
    res = requests.get(url)
    if res.status_code == 500:
        return False
    else:
        ## bot.send_photo(chat_id=msg.chat_id, photo=url)
        img_meteo = BytesIO(urlopen(url).read())
        img_meteo.name = 'img_meteo.jpeg'
        img_meteo.seek(0)
    return(img_meteo)

def start(bot, update):
    """ Start (callback funtion)
    Args:   bot, the bot
            update, update message
    Return: -
    """
    bot.send_message(chat_id=update.message.chat_id, parse_mode='HTML',
                     text="""Bonjour,
Je suis un robot, connaissant bien la météo, pour une savoir 
plus faites : <b>/usage</b>
""")
    ##bot.send_message(chat_id=update.message.chat_id, text=update.message.first_name)

def meteo(bot, update):
    """ meteo (callback function    )

    get triggered by /meteo messages

    tokenize message, extract city name, get the meteo and replies with the 
    corresponding image
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
    img_meteo = get_meteo(ville, day)
    if img_meteo:
        bot.send_photo(chat_id=msg.chat_id, photo=img_meteo)
    else:
        alternate_cities = possible_cities(ville)
        txt = "Désolé, ville inconnue, essayez celle-ci:\n"
        for city in alternate_cities:
            txt += "pour " + alternate_cities[city] + " utiliser: " + city + "\n"
        bot.send_message(chat_id=msg.chat_id, text=txt)

def usage(bot, update):
    """ help (callback function)

    callback to the /usage message
    replies with an usage message.
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

    answer to /cities command

    replies with list of cities known in the configuration file.
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
