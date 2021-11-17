# A Crypto Ticker for the inkyphat 212x104 

![dimeinky](https://user-images.githubusercontent.com/75382474/142042179-8a3e642e-ee83-4a61-b024-6bd6d966e56f.jpg)

Inky pHat can be found here:</br>
https://shop.pimoroni.com/products/inky-phat?variant=12549254217811 </br>
https://www.adafruit.com/product/3743

This little app currently supports <a href="https://www.dimecoinnetwork.com">Dimecoin</a>, Bitcoin, Ethereum, Cardano, and Doge.</br>
The coin prices are updated on a configurable time within config.json.  The default is every 30 minutes.  Please note that the free API access with CoinMarketCap is limited to about 300 requests per day.  So if you're querying 5 different coins every 1800 seconds (30 minutes) that's 240 API calls per day.  

1. Attach the Inky device to your Raspberry Pi and make sure SPI is enabled: sudo raspi-config
2. Download the Code: git clone https://github.com/prettyflyforabeeguy/InkyTicker.git
3. Install the inky phat library: pip3 install inkyphat
4. Generate your own API key for coinmarketcap: https://coinmarketcap.com/api/
5. Add your API key to ./config/config.json and save your changes
6. Run the program: python3 inkyticker.py

Pro Tips: 
1. Want to add more coins?
Create a 50 pixel x 50 pixel image of your coin and place this .png file in the img folder.  Be sure to name the file exactly the same as the coin ticker.  The image mode should be RGB 8/bit and the only supports Red, Black, and White colors.  Then in your config.json just add the new coin ticker to the list.

2. Want to change the currency?
Just change the "USD" in the config.json to your desired currency i.e. GBP.  If it's a supported currency with coinmarketcap it should work.

Enjoy!
