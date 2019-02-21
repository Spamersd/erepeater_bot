# -*- coding: utf-8 -*-
import config #add config.py file in current directory 
import telebot
import imaplib
import email
import time
import logging

from time import sleep
from telebot import apihelper
from bs4 import BeautifulSoup

apihelper.proxy = {'https':'socks5://localhost:9050'}

FORMAT = "%(asctime)s;%(levelname)s;%(message)s"

logging.basicConfig(filename="bot.log", level=logging.INFO, format=FORMAT)

bot = telebot.TeleBot(config.token)

def check_email():

    imap = imaplib.IMAP4(config.IMAP_SERVER,config.IMAP_PORT)
    imap.login(config.IMAP_LOGIN,config.IMAP_PASSWORD)
    imap.select()
    typ, mails = imap.search(None, 'ALL') 

    for num in mails[0].split(): 
        typ, data = imap.fetch(num, "(RFC822)") 
        message = parse_message(data)

        if sendbot(message):
            imap.store(num, '+FLAGS', '\\Deleted')
            pass     

    imap.expunge()             
    imap.close() 
    imap.logout() 
    pass

def parse_message(data):

    msg = email.message_from_bytes(data[0][1],
     _class = email.message.EmailMessage)

    msg_date = msg.get('Date')
    msg_from = getHeader(msg,'From')
    msg_subject = getHeader(msg,'Subject')
    msg_body = getBody(msg)
    msg = cut_message(msg_date + '\n' + msg_from +'\n' + msg_subject +'\n'+ msg_body)
    
    return msg
    pass

def cut_message (msg):
    while "  " in msg:
        msg= msg.replace("  ", " ")

    msg = msg.expandtabs(1)
    msg = msg.strip()
    if len(msg) > 500:
        msg = msg[0:500]

    return msg
    pass

def getBody(msg):
    """ Extract content body of an email messsage """
    try:
        if msg.is_multipart():
            body = ""
            for payload in msg.get_payload():
                body = body + getBody(payload)

        else:
            charset = msg._charset
            if charset is None:
                charset = 'utf-8' 
            body = msg.get_payload(decode=True).decode(charset)
            soup = BeautifulSoup(body)
            return soup.get_text()  
        pass
    except Exception as e:
        body = "Ошибка обработки тела письма" + str(e)
        logging.error(body)
        pass
    
    return body

def getHeader(Message,Attribute):
    
    text = ""
    
    try:
        encoding_header = Message.get(Attribute)
        decoding_header = email.header.decode_header(encoding_header)

        for a in decoding_header:

            str_text, str_encoding = a

            if str_encoding is None : 
                str_encoding = "utf-8"
                pass
            if isinstance(str_text,bytes):
                text = text + str_text.decode(str_encoding)
                pass
            elif  isinstance(str_text,str):
                text = text + str_text                
                pass
            pass

        pass
    except Exception as e:
        pass   
    
    return text
    pass

def sendbot(msg):
    
    result = True

    try:
        bot.send_message(config.CHANNEL_NAME, msg)
        pass
    except Exception as e:
        logging.error("Error send message from bot" + str(e))
        result = False
        pass
    return result
    pass

if __name__ == '__main__':

    logging.info("Bot was started")

    while True:
        try:
            check_email()
        except Exception as e:
            sendbot("Ошибка проверки почты!\n"+"Ошибка: "+str(e))
            logging.error("Error check email: "+ str(e))
        time.sleep(300)
        pass

