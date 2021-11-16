#!/usr/bin/env python3

# A simple template for using the Red/Black/White InkyPhat resoultion 212x104

from PIL import Image, ImageFont, ImageDraw
import inkyphat
import time, datetime
import requests

class InkyPi():
    def __init__(self):
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
        # draw rectangle zones for the display
        inkyphat.rectangle([(0, 0), (212, 104)], fill=inkyphat.WHITE, outline=None)  # Clear Screen
        inkyphat.rectangle([(57, 23), (210, 104)], fill=inkyphat.RED, outline=None)  # Price Zone
        inkyphat.rectangle([(57, 1), (210, 23)], fill=inkyphat.WHITE, outline=None)  # Title Bar
        inkyphat.rectangle([(54, 1), (55, 104)], fill=inkyphat.BLACK, outline=None)  # Vertical Line

    def getPrice(self, symbol, currency):
        base_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?"
        url = base_url + "symbol=" + symbol + "&convert=" + currency
        # Set headers
        headers = {
            "X-CMC_PRO_API_KEY" : "",
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
        #price = round(price, 2)
        price = f'{price:.10f}'
        return price


    def setLogo(self, path, ticker, pair):
        logo = Image.open(path)
        coin =  ticker + "\n -\n " + pair
        inkyphat.text((2, 3), coin, inkyphat.BLACK, font=self.fontPressStart2P)
        inkyphat.paste(logo,(2, 50))

    def displayPrice(self, price):
        inkyphat.rectangle([(57, 23), (210, 104)], fill=inkyphat.RED, outline=None)  # Clear the price zone
        inkyphat.text((59, 50), price, inkyphat.WHITE, font=self.fontPressStart2P_large)

    def getTextSize(self, h, font, txt):
        # Calculate the positioning and draw the text
        txt_w, txt_h = font.getsize(txt)
        txt_x = int((self.inky_display.width - txt_w) / 2)
        txt_y = h + self.padding
        #txt_y = int(y_top + ((y_bottom - y_top - name_h) / 2))  #Place text within white text bar
        #self.draw.text((txt_x, txt_y), txt, self.inky_display.BLACK, font=font)
        return txt_x, txt_y, txt_h


if __name__ == '__main__':
    iph = InkyPi()

    #iph.setLogo("./img/dimecoin_logo_black.png","DIME", "USD")
    iph.setLogo("./img/BTC_logo.png","BTC", "USD")

    while True:
        inkyphat.rectangle([(57, 1), (210, 23)], fill=inkyphat.WHITE, outline=None) # Clear the title bar
        title = str(datetime.datetime.now())
        inkyphat.text((60, 3), title, inkyphat.BLACK, font=iph.fontFredokaOne)

       #price = iph.getPrice("DIME", "USD")
        price = iph.getPrice("BTC", "USD")

        print(price)
        iph.displayPrice(str(price))
        inkyphat.show()
        time.sleep(600)

