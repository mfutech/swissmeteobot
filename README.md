
# Swiss Meteo Bot

this is a Telegram bot, helping retrieving meteo information. 
The Bot speaks french for the time being, it does understand english 
command and really need to be upgraded to german, but will take a little
while.

If you want to test it live, open Telegram and send /usage to @SwissMeteoBot.

There are also required files to build a docker image.


## Using the docker image

   1. create a Telegram bot
   2. copy config.example.yml to config.yml and update the token entry 
   with your bot token
   3. then just: 
   ```
   $ docker -t my_meteo_bot build .`
   $ docker run my_meteo_bot
   ```


## source of the meteo informaton

Meteo is coming from http://www.prevision-meteo.ch.
They authorize the inclusing of their images to other website. The bot is doing the same, downloading the required image and sending to the user requesting it.

*Please respect prevision-meteo.ch terms of service*