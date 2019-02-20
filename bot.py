# -*- coding: utf-8 -*-
import config #add config.py file in current directory 
import telebot
import imaplib
import email
import time

from time import sleep
from telebot import apihelper
from bs4 import BeautifulSoup


apihelper.proxy = {'https':'socks5://localhost:9050'}

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
    msg = msg_date + '\n' + msg_from +'\n' + msg_subject +'\n'+ msg_body 

    return msg
    pass

def getBody(msg):
    """ Extract content body of an email messsage """
    body = ""
    if msg.is_multipart():
        for payload in msg.get_payload():
            charset = payload._charset
            if charset is None:
                charset = 'utf-8' 
            # if payload.is_multipart(): ...
            body = body + payload.get_payload(decode=True).decode(charset)
    else:
        charset = msg._charset
        if charset is None:
            charset = 'utf-8' 
        body = msg.get_payload(decode=True).decode(charset)

    soup = BeautifulSoup(body)
    return soup.get_text()

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
    except:
        pass   
    
    return text
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

     while True:
        try:
            check_email()
        except:
            sendbot("Ошибка проверки почты!")
        time.sleep(60)
        pass

