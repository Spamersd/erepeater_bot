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
            pass
           # imap.store(num, '+FLAGS', '\\Deleted')    

    imap.expunge()             
    imap.close() 
    imap.logout() 

def parse_message(data):

    msg = email.message_from_bytes(data[0][1],_class = email.message.EmailMessage)

    msg_date = msg.get('Date')
    msg_from = get_header(msg,'From')
    msg_subject = get_header(msg,'Subject')
    msg_body = get_body(msg)
    msg = cut_message(msg_date + '\n' + msg_from +'\n' + msg_subject +'\n'+ msg_body)
    
    return msg

def cut_message (msg):
    
    while "  " in msg:
        msg= msg.replace("  ", " ")

    msg = msg.expandtabs(1)
    msg = msg.strip()
    msg = msg[:500]

    return msg
 
def get_body(msg):
    
    try:
        if msg.is_multipart():
            body = ''.join([get_body(payload) for payload in msg.get_payload()])

        else:
            charset = msg._charset
            if charset is None:
                charset = 'utf-8' 
            body = msg.get_payload(decode=True).decode(charset)
            soup = BeautifulSoup(body)
            return soup.get_text()  
    
    except Exception as e:
        body = f"Error processing body\nError: {str(e)}"
        logging.error(body)
    
    return body

def get_header(Message,Attribute):
    
    text = ""
    
    try:
        encoding_header = Message.get(Attribute)
        decoding_header = email.header.decode_header(encoding_header)

        for a in decoding_header:

            str_text, str_encoding = a

            if str_encoding is None : 
                str_encoding = "utf-8"
            if isinstance(str_text,bytes):
                text = text + str_text.decode(str_encoding)
            elif  isinstance(str_text,str):
                pass

    except Exception as e:
        pass
    return text

def sendbot(msg):
    
    try:
        bot.send_message(config.CHANNEL_NAME, msg)
    except Exception as e:
        logging.error(f"Error send message from bot {str(e)}")
        return False
    else:
        return True

if __name__ == '__main__':

    logging.info("Bot was started")

    while True:
        try:
            check_email()
        except Exception as e:
            sendbot(f"Error check email!\nError: {str(e)}")
            logging.error(f"Error check email: {str(e)}")
        time.sleep(300)


