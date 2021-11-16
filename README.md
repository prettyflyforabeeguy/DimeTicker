# A Crypto Ticker for the inkyphat 212x104 

![inky](https://user-images.githubusercontent.com/75382474/142041258-e2ad059f-931f-4160-961d-cf2af28c5380.jpg)

Inky pHat can be found here:</br>
https://shop.pimoroni.com/products/inky-phat?variant=12549254217811 </br>
https://www.adafruit.com/product/3743

This little app currently supports Dimecoin, Bitcoin, and Ethereum.</br>
The coin prices are updated every 10 minutes.

1. Attach the Inky device to your Raspberry Pi and make sure SPI is enabled: sudo raspi-config
2. Download the Code: git clone https://github.com/prettyflyforabeeguy/InkyTicker.git
3. Install the inky phat library: pip3 install inkyphat
4. Generate your own API key for coinmarketcap: https://coinmarketcap.com/api/
5. Add your API key to ./config/config.json and save your changes
6. Run the program: python3 inkyticker.py

Enjoy!
