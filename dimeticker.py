#!/usr/bin/env python3

# A simple crypto ticker app using the Red/Black/White InkyPhat resoultion 212x104
# created by prettyflyforabeeguy https://github.com/prettyflyforabeeguy/DimeTicker
# Logo images should be 50px x 50px RGB mode

from PIL import Image, ImageFont, ImageDraw
import inkyphat
import time, datetime
import requests
import config as _cfg

class DimeTicker():
    def __init__(self):
        self.config_dict = _cfg.Config().config_dict
        self.cmcKey = _cfg.Config().config_vsearch(self.config_dict, "CoinMarketCapKey")
        self.coinList = self.config_dict["Coins"]
        self.currencyList = self.config_dict["Currency"]
        self.rotateScreen = self.config_dict["RotateScreen"]
        self.qInterval = self.config_dict["QueryInterval"]

        # setup fonts
        self.fsAmaticSCBold = 12
        self.fontAmaticSCBold = ImageFont.truetype(inkyphat.fonts.AmaticSCBold, self.fsAmaticSCBold)
        self.fsAmaticSC = 12
        self.fontAmaticSC = ImageFont.truetype(inkyphat.fonts.AmaticSC, self.fsAmaticSC)
        self.fsFredokaOne = 12
        self.fontFredokaOne = ImageFont.truetype(inkyphat.fonts.FredokaOne, self.fsFredokaOne)
        self.fsPressStart2P = 12
        self.fsPressStart2P_large = 14
        self.fontPressStart2P = ImageFont.truetype(inkyphat.fonts.PressStart2P, self.fsPressStart2P)
        self.fontPressStart2P_large = ImageFont.truetype(inkyphat.fonts.PressStart2P, self.fsPressStart2P_large)
        self._response = None

        self.phatSetup()

    def phatSetup(self):
        inkyphat.set_border(inkyphat.BLACK)
        inkyphat.set_colour('red')
        if self.rotateScreen == True:
            inkyphat.set_rotation(180)

        # draw rectangle zones for the display
        inkyphat.rectangle([(0, 0), (212, 104)], fill=inkyphat.WHITE, outline=None)   # Clear Screen
        inkyphat.rectangle([(57, 23), (210, 104)], fill=inkyphat.WHITE, outline=None) # Price Zone
        inkyphat.rectangle([(57, 1), (210, 23)], fill=inkyphat.WHITE, outline=None)   # Title Bar
        inkyphat.rectangle([(54, 1), (55, 104)], fill=inkyphat.BLACK, outline=None)   # Vertical Line

    def getPrice(self, symbol, currency):
        base_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?"
        url = base_url + "symbol=" + symbol + "&convert=" + currency
        # Set headers
        headers = {
            "X-CMC_PRO_API_KEY" : self.cmcKey,
            "Accept" : "application/json"
        }
        # Request body
        requestBody = {
        }
        try:
            self._response = requests.get(url, headers=headers, data=requestBody)  #Execute the API and store the response.
        except Exception as e:
            print(e)

        price = float(self._response.json()["data"][symbol]["quote"][currency]["price"])
        hr_change = float(self._response.json()["data"][symbol]["quote"][currency]["percent_change_1h"])
        hr_change = f'{hr_change:.2f}'
        if price > 1:
            #price = round(price, 2)
            price = f"{price:,.2f}"

        else:
            price = f'{price:.10f}'
            #price = "{:,.10f}".format(price)

        return price, hr_change

    def setLogo(self, path, ticker, pair):
        inkyphat.rectangle([(0, 0), (212, 104)], fill=inkyphat.WHITE, outline=None)  # Clear Screen
        inkyphat.rectangle([(54, 1), (55, 104)], fill=inkyphat.BLACK, outline=None)  # Vertical Line
        logo = Image.open(path)
        coin =  ticker + "\n -\n " + pair
        inkyphat.text((2, 3), coin, inkyphat.BLACK, font=self.fontPressStart2P)
        inkyphat.paste(logo,(2, 50))

    def displayPrice(self, price, hr_change):
        inkyphat.rectangle([(57, 23), (210, 104)], fill=inkyphat.WHITE, outline=None)  # Clear the price zone
        inkyphat.text((59, 45), price, inkyphat.BLACK, font=self.fontPressStart2P_large)

        if float(hr_change) < 0:
            color = inkyphat.RED
            down = Image.open('./img/down_arrow.png')
            inkyphat.paste(down,(160, 62))
        else:
            color = inkyphat.BLACK
            up = Image.open('./img/up_arrow.png')
            inkyphat.paste(up,(160, 20))


        hr_change = "Change in last hr: " + str(hr_change) + "%"
        inkyphat.text((71, 88), hr_change, color, font=self.fontFredokaOne)


if __name__ == '__main__':
    dt = DimeTicker()
    c_len = len(dt.coinList)

    while True:
        #for each coin in coinlist, set logo and text, run the API, display everything, then sleep
        for i in range(c_len):
            dt.setLogo("./img/" + dt.coinList[i] + ".png",dt.coinList[i], dt.currencyList[0])
            inkyphat.rectangle([(57, 1), (210, 23)], fill=inkyphat.WHITE, outline=None) # Clear the title bar
            title = str(datetime.datetime.now())
            inkyphat.text((60, 3), title, inkyphat.BLACK, font=dt.fontFredokaOne)

            price, hr_change = dt.getPrice(dt.coinList[i], dt.currencyList[0])

            print(f"{dt.coinList[i]} price: {price} {dt.currencyList[0]}")
            print(f"Percent Change in the last hour: {hr_change}%")
            dt.displayPrice(str(price), str(hr_change))
            inkyphat.show()
            time.sleep(5)
        time.sleep(dt.qInterval)
