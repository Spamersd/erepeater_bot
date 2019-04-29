#/bin/bash
echo "nameserver 8.8.8.8" > /etc/resolv.conf    
tor & python3 bot.py