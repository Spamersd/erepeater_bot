# -*- coding: utf-8 -*-
import config #add config.py file in current directory 
import telebot
import imaplib
import email
import time

from time import sleep
from telebot import apihelper

apihelper.proxy = {'https':'socks5://localhost:9050'}

bot = telebot.TeleBot(config.token)

def check_email():

    imap = imaplib.IMAP4(config.IMAP_SERVER,config.IMAP_PORT)
    imap.login(config.IMAP_LOGIN,config.IMAP_PASSWORD)
    imap.select()
    typ, mails = imap.search(None, 'ALL') 

    for num in mails[0].split(): 
        typ, data = imap.fetch(num, "(RFC822)") 
        msg = email.message_from_bytes(data[0][1], _class = email.message.EmailMessage)
        payload = msg.get_payload()
        if sendbot(payload):
            imap.store(num, '+FLAGS', '\\Deleted')
            pass     

    imap.expunge()             
    imap.close() 
    imap.logout() 
    pass

def sendbot(msg):
    result = True
    try:
        bot.send_message(config.CHANNEL_NAME, msg)
        pass
    except:
        print("Ошибка отправки собщения ботом")
        result = False
        pass
    return result
    pass


if __name__ == '__main__':
    print('Bot is started!')
    while True:
        try:
            check_email()
        except:
            sendbot("Ошибка проверки почты!")
        time.sleep(120)
        pass

