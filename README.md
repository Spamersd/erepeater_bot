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
 --build-arg TOKEN='"6757123123123:fjklsdfjkhsdfjh"'\
 --build-arg CHANNEL_NAME='"1231234"'\
 --build-arg IMAP_SERVER='"127.0.0.1"'\
 --build-arg IMAP_PORT='"110"'\
 --build-arg IMAP_LOGIN='"test@test.com"'\
 --build-arg IMAP_PASSWORD='"password"'\
 ```
