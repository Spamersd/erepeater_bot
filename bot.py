# -*- coding: utf-8 -*-
import telebot
import imaplib
import email
import time
import logging

from time import sleep
from telebot import apihelper
from bs4 import BeautifulSoup

import config #add config.py file in current directory 

apihelper.proxy = {'https':'socks5://localhost:9050'}

FORMAT = "%(asctime)s;%(levelname)s;%(message)s"

logging.basicConfig(filename="bot.log", level=logging.INFO, format=FORMAT)

bot = telebot.TeleBot(config.TOKEN)

class ImapHendler:
    
    config = None

    imap =None
    
    def __init__(self,config):
        self.config = config
        self.imap = imaplib.IMAP4(config.IMAP_SERVER,config.IMAP_PORT)
        super().__init__()
    
    def connect(self):
        try:
            self.imap.login(self.config.IMAP_LOGIN,self.config.IMAP_PASSWORD)     
        except Exception as e:
            logging.error(f"Error: {(e)}")

    def check_email(self):

        self.imap.select()
        typ, mails = self.imap.search(None, 'ALL') 

        for num in mails[0].split(): 
            typ, data = self.imap.fetch(num, "(RFC822)") 
            message = parse_message(data)

            if send_bot(message):
                imap.store(num, '+FLAGS', '\\Deleted')    

        self.imap.expunge() 

    def state(self):
        return self.imap.state

    def close(self):
        self.imap.close()
    
    def logout(self):
        self.imap.logout()     

def parse_message(data):

    msg = email.message_from_bytes(data[0][1], \
    _class = email.message.EmailMessage)

    msg_date = msg.get('Date')
    msg_from = get_header(msg,'From')
    msg_subject = get_header(msg,'Subject')
    msg_body = extract_body(msg)
    msg = cut_message(msg_date + '\n' + \
        msg_from +'\n' + msg_subject +'\n'+ msg_body)
    
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
            body = ''.join([get_body(payload) \
                for payload in msg.get_payload()])

        else:
            if msg._charset is None:
                body = msg.get_payload(decode=True).decode()
            else:
                body = msg.get_payload(decode=True).decode(msg._charset) 
           
            soup = BeautifulSoup(body)
            return soup.get_text()  
    
    except Exception as e:
        body = f"Error processing body\nError: {str(e)}"
        logging.error(body)
    
    return body

def extract_body(msg, depth=0):
    try:
        """ Extract content body of an email messsage """
        body = []
        if msg.is_multipart():
            main_content = None
            # multi-part emails often have both
            # a text/plain and a text/html part.
            # Use the first `text/plain` part if there is one,
            # otherwise take the first `text/*` part.
            for part in msg.get_payload():
                is_txt = part.get_content_type() == 'text/plain'
                if not main_content or is_txt:
                    main_content = extract_body(part)
                if is_txt:
                    break
            if main_content:
                body.extend(main_content)
        elif msg.get_content_type().startswith("text/"):
            # Get the messages
            charset = msg.get_param('charset', 'utf-8').lower()
            # update charset aliases
            charset = email.charset.ALIASES.get(charset, charset)
            msg.set_param('charset', charset)
            try:
                body.append(msg.get_content())
            except AssertionError as e:
                print('Parsing failed.    ')
                print(e)
            except LookupError:
                # set all unknown encoding to utf-8
                # then add a header to indicate this might be a spam
                msg.set_param('charset', 'utf-8')
                body.append('=== <UNKOWN ENCODING POSSIBLY SPAM> ===')
                body.append(msg.get_content())
        return body
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
        logging.error(f"Error:{(e)}")
        pass
    return text

def send_bot(msg):
    
    try:
        bot.send_message(config.CHANNEL_NAME, msg)
    except Exception as e:
        logging.error(f"Error send message from bot {str(e)}")
        return False
    else:
        return True

if __name__ == '__main__':

    logging.info("Bot was started")
    ImapSession = ImapHendler(config)
    ImapSession.connect()

    while True:
        try:
            if ImapSession.state() == 'AUTH':
                ImapSession.check_email()
            else:
                ImapSession.connect()
                ImapSession.check_email()
        except Exception as e:
            logging.error(f"Error check email: {str(e)}")
    
        #time.sleep(300)
    
    ImapSession.close() 
    ImapSession.logout()