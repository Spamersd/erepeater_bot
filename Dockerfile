FROM python:3.6

RUN apt-get update;\
    apt-get install tor;\
    apt-get install pyton3-pip;

RUN  pip install pytelegrambotapi;\
     curl -O https://raw.githubusercontent.com/Spamersd/erepeater_bot/master/bot.py;

ENTRYPOINT python3 bot.py