Telegram bot
=====================

Description
---------------------
The program reads messages sent to the specified e-mail address and sends it to the specified telegram channel. To bypass locks in Russia, the tor network is used. The whole program works as a separate Docker container.

System preparation
---------------------
Required to register a bot telegram.
Requires Docker installed.
To start the system, copy the Dockerfile to the local system.

How to use
---------------------
```
docker build -t spamersd/tbot .\
 --build-arg TOKEN='"675791820:AAH5hX3iaR2eSpAfSp1RfYVidCZ6nb_pfGw"'\
 --build-arg CHANNEL_NAME='"191031865"'\
 --build-arg IMAP_SERVER='"192.168.1.7"'\
 --build-arg IMAP_PORT='"143"'\
 --build-arg IMAP_LOGIN='"test@krasgaz.ru"'\
 --build-arg IMAP_PASSWORD='"jun0vaf396"'\
 ```
