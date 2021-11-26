#!/usr/bin/env python3

# A simple crypto ticker app using the Red/Black/White InkyPhat resoultion 250x122
# This is for the newer Inky pHAT SSD1608
# created by prettyflyforabeeguy https://github.com/prettyflyforabeeguy/DimeTicker
# Logo images should be 50px x 50px RGB mode

from PIL import Image, ImageFont, ImageDraw
import inkyphat
import time, datetime, sys
import requests
import config as _cfg

from font_fredoka_one import FredokaOne
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky.auto import auto

inky_display = auto(ask_user=True, verbose=True)
img = Image.new("P", inky_display.resolution)
draw = ImageDraw.Draw(img)

class DimeTicker():
    def __init__(self):
        self.config_dict = _cfg.Config().config_dict
        self.cmcKey = _cfg.Config().config_vsearch(self.config_dict, "CoinMarketCapKey")
        self.coinList = self.config_dict["Coins"]
        self.currencyList = self.config_dict["Currency"]
        self.rotateScreen = self.config_dict["RotateScreen"]
        self.qInterval = self.config_dict["QueryInterval"]

        # setup fonts
        self.intuitive_font = ImageFont.truetype(Intuitive, int(14 * 1.30))
        self.smfredoka_one_font = ImageFont.truetype(FredokaOne, int(12 * 1.30))
        self.fredoka_one_font = ImageFont.truetype(FredokaOne, int(16 * 1.30))
        self.lgfredoka_one_font = ImageFont.truetype(FredokaOne, int(22 * 1.30)) 
        self.hanken_groteskmed_font = ImageFont.truetype(HankenGroteskMedium, int(12 * 1.30))
        self.hanken_groteskbld_font = ImageFont.truetype(HankenGroteskBold, int(10 * 1.30))

        self._response = None

        self.phatSetup()

    def phatSetup(self):
        img = Image.new("P", inky_display.resolution)
        draw = ImageDraw.Draw(img)

        inky_display.set_border(inky_display.BLACK)
        if self.rotateScreen == True:
            inky_display.set_rotation(180)


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
        logo = Image.open(path)
        coin =  ticker + "\n   -\n " + pair
        draw.text((2, 3), coin, inky_display.BLACK, font=self.smfredoka_one_font)
        blank = Image.open("./img/blank.png")
        img.paste(blank,(2, 70))  # Attempt to clear some background pixels with a blank image.
        img.paste(logo,(2, 70))


    def displayPrice(self, price, hr_change):
        if float(hr_change) < 0:
            color = inky_display.RED
            draw.text((60, 45), price, color, font=self.lgfredoka_one_font)
            down = Image.open('./img/down_arrow.png')
            img.paste(down,(190, 82))
        else:
            color = inky_display.BLACK
            draw.text((60, 45), price, color, font=self.lgfredoka_one_font)
            up = Image.open('./img/up_arrow.png')
            img.paste(up,(190, 25))

        hr_change = "Change in last hr: " + str(hr_change) + "%"
        draw.text((100, 105), hr_change, color, font=self.hanken_groteskbld_font)


    def splashScreen(self, path):
        img = Image.new("P", inky_display.resolution)
        draw = ImageDraw.Draw(img)

        qr = Image.open(path)
        img.paste(qr, (5, 10))

        draw.text((100, 2), "DIMEcoin", inky_display.BLACK, font=self.fredoka_one_font)
        draw.text((88, 25), "The Global Payment", inky_display.BLACK, font=self.hanken_groteskmed_font)

        draw.text((88, 45), "Solution!", inky_display.BLACK, font=self.hanken_groteskmed_font)
        draw.text((88, 66), "Learn more at:", inky_display.BLACK, font=self.hanken_groteskbld_font)
        draw.text((88, 78), "www.dimecoinnetwork.com", inky_display.BLACK, font=self.hanken_groteskbld_font)

        draw.text((95, 105), "Starting up DimeTicker...", inky_display.RED, font=self.hanken_groteskbld_font)

        inky_display.set_image(img)
        inky_display.show()


    def donations(self, path):
        img = Image.new("P", inky_display.resolution)
        draw = ImageDraw.Draw(img)

        donations = Image.open(path)
        img.paste(donations, (1, 1))

        draw.text((4, 60), "DIME", inky_display.BLACK, font=self.fredoka_one_font)
        draw.text((87, 60), "BTC", inky_display.BLACK, font=self.fredoka_one_font)
        draw.text((162, 60), "ETH", inky_display.BLACK, font=self.fredoka_one_font)

        draw.text((4, 90), "Donations are welcome!", inky_display.BLACK, font=self.hanken_groteskmed_font)
        draw.text((4, 105), "Thank you for using DimeTicker!", inky_display.RED, font=self.hanken_groteskbld_font)

        inky_display.set_image(img)
        inky_display.show()



if __name__ == '__main__':
    dt = DimeTicker()
    c_len = len(dt.coinList)

    dt.splashScreen("./img/dimeNetworkqr_small.png")
    time.sleep(10)
    try:
        while True:
            #for each coin in coinlist, set logo and text, run the API, display everything, then sleep
            for i in range(c_len):
                img = Image.new("P", inky_display.resolution)
                draw = ImageDraw.Draw(img)
                draw.rectangle((54, 1, 56, 122), fill=inky_display.BLACK, outline=None)

                dt.setLogo("./img/" + dt.coinList[i] + ".png",dt.coinList[i], dt.currencyList[0])
                title = str(datetime.datetime.now())
                draw.text((60, 3), title, inky_display.BLACK, font=dt.hanken_groteskbld_font)

                price, hr_change = dt.getPrice(dt.coinList[i], dt.currencyList[0])

                print(f"{dt.coinList[i]} price: {price} {dt.currencyList[0]}")
                print(f"Percent Change in the last hour: {hr_change}%")
                dt.displayPrice(str(price), str(hr_change))

                inky_display.set_image(img)
                inky_display.show()
                time.sleep(120)
            time.sleep(dt.qInterval)

    except KeyboardInterrupt:
        # Exit
        donate = """Want to see more cool stuff like this? Your dontations are always welcome!
DIME: 7JwbNZdP3pzreem3v3rmWAXcP5LxvqRTgU
BTC: bc1q3m4x0d8j6c8enkzeet2c4tcy26uflsm9s4njg4
LTC: ltc1qzhavlsq29kqe65cjjuq2l23d92f0mqlwkwldrg
ETH: 0xaf9dB0Eaf3A398A4F549A09e1230B42B51FdAFF3"""
        print(donate)
        print("Thank you for using DimeTicker. Goodbye!")
        #dt.donations("./img/donations.png")
        sys.exit()

