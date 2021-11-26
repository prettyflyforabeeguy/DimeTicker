# A Crypto Ticker for the inkyphat 212x104 and 250x122 

![DimeTicker](https://user-images.githubusercontent.com/75382474/142347905-30446d59-735b-47f7-80fb-7ace743d8434.jpg)

This little crypto app currently supports <a href="https://www.dimecoinnetwork.com">Dimecoin</a>, Bitcoin, Ethereum, Cardano, and Doge.</br>
The coin prices are updated on a configurable time within config.json.  The default is every 30 minutes.  Please note that the free API access with CoinMarketCap is limited to about 300 requests per day.  So if you're querying 5 different coins every 1800 seconds (30 minutes) that's 240 API calls per day.  

Inky pHat can be found here:</br>
https://shop.pimoroni.com/products/inky-phat?variant=12549254217811 </br>
https://www.adafruit.com/product/3743

<b>IMPORTANT:</b> </br>
Pimoroni makes 2 models of the Inky pHat. While they look identical on the outside, they come in 2 different resolutions and use totally different libraries. </br>
212x104 Hight-Temp </br>
250x122 SSD1608 (newer) </br>

<b>SETUP: </b> </br>
1. Attach the Inky device to your Raspberry Pi and make sure SPI is enabled: sudo raspi-config
2. Install the inky library:</br> 
      For 212x104: Install the inky phat library: pip3 install inkyphat </br>
      For 250x122: curl https://get.pimoroni.com/inky | bash </br>
3. Download the Code: git clone https://github.com/prettyflyforabeeguy/DimeTicker.git
4. Generate your own API key for coinmarketcap: https://coinmarketcap.com/api/
5. Add your API key between the quotes in ./config/config.json and save your changes
6. Run the program:</br> 
      For 212x104: python3 ticker.py </br>
      For 250x122: python3 ticker2.py </br>

<b>Pro Tips: </b> </br> 
1. Want to add more coins?
Create a 50 pixel x 50 pixel image of your coin and place this .png file in the img folder.  Be sure to name the file exactly the same as the coin ticker.  The image mode should be RGB 8/bit and the only supports Red, Black, and White colors.  Then in your config.json just add the new coin ticker to the list.
Not comfortable with this? No prob, just copy the img\blank.png to what ever coin you want.
i.e. cp blank.png LTC.png
Now when you add LTC to your config.json it will have a blank logo but will still retrieve the price and everything.

2. Want to change the currency?
Just change the "USD" in the config.json to your desired currency i.e. GBP.  If it's a supported currency with coinmarketcap it should work.

<b>Final Notes:</b> </br>
Currently screen rotation is not supported in the 250x122 ticker2.py code but is supported in the 212x104 ticker.py code.

Enjoy!

Many thanks to <a href="https://www.thingiverse.com/3mul0r/designs">3mul0r</a> for his awesome raspberry pi zero inky case design.


If you found this useful, donations are always appreciated:</br>
DIME: 7JwbNZdP3pzreem3v3rmWAXcP5LxvqRTgU  </br>
BTC:  bc1q3m4x0d8j6c8enkzeet2c4tcy26uflsm9s4njg4 </br>
LTC:  ltc1qzhavlsq29kqe65cjjuq2l23d92f0mqlwkwldrg </br>
ETH:  0xaf9dB0Eaf3A398A4F549A09e1230B42B51FdAFF3 </br>
