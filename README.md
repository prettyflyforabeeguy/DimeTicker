# A Crypto Ticker for the inkyphat 212x104 
https://shop.pimoroni.com/products/inky-phat?variant=12549254217811
https://www.adafruit.com/product/3743

This app currently supports Dimecoin, Bitcoin, and Ethereum
The coin prices are updated every 10 minutes.

1. Attach the Inky device to your Raspberry Pi
2. Make sure it's enabled: sudo raspi-config
3. Download the Code: git clone https://github.com/prettyflyforabeeguy/InkyTicker.git
4. Install the inky phat library: pip3 install inkyphat
5. Generate your own API key for coinmarketcap: https://coinmarketcap.com/api/
6. Add your API key to ./config/config.json and save your changes
7. Run the program: python3 inkyticker.py

Enjoy!
