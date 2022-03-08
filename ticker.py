#!/usr/bin/env python3

# A simple crypto ticker app using the Red/Black/White InkyPhat resoultion 212x104
# created by prettyflyforabeeguy https://github.com/prettyflyforabeeguy/DimeTicker
# Logo images should be 50px x 50px RGB mode

from PIL import Image, ImageFont, ImageDraw
import inkyphat
import time, datetime, sys
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

        except Exception as e:
            print(e)
            #inkyphat.rectangle([(0, 0), (212, 104)], fill=inkyphat.WHITE, outline=None)  # Clear Screen
            #inkyphat.text((5, 64), "Something is wrong with coinmarketcaps API", inkyphat.BLACK, font=self.fontPressStart2P)
            #inkyphat.text((5, 77), "Reboot your raspberry pi!", inkyphat.BLACK, font=self.fontFredokaOne)
            print(f"EXCEPTION OCCURED\n {e}")
            print(f"\nCMC is taking too long to lookup {symbol}.  Skipping...")
            pass

    def setLogo(self, path, ticker, pair):
        inkyphat.rectangle([(0, 0), (212, 104)], fill=inkyphat.WHITE, outline=None)  # Clear Screen
        inkyphat.rectangle([(54, 1), (55, 104)], fill=inkyphat.BLACK, outline=None)  # Vertical Line
        logo = Image.open(path)
        coin =  ticker + "\n -\n " + pair
        inkyphat.text((2, 3), coin, inkyphat.BLACK, font=self.fontPressStart2P)
        blank = Image.open("./img/blank.png")
        inkyphat.paste(blank,(2, 50))  # Attempt to clear some background pixels with a blank image.
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


    def splashScreen(self, path):
        inkyphat.rectangle([(0, 0), (212, 104)], fill=inkyphat.WHITE, outline=None)  # Clear Screen
        qr = Image.open(path)
        inkyphat.paste(qr, (5, 10))
        inkyphat.text((100, 2), "DIMEcoin", inkyphat.BLACK, font=self.fontPressStart2P)
        inkyphat.text((88, 15), "The Global Payment", inkyphat.BLACK, font=self.fontFredokaOne)
        inkyphat.text((88, 28), "Solution!", inkyphat.BLACK, font=self.fontFredokaOne)

        inkyphat.text((88, 51), "Learn more at:", inkyphat.BLACK, font=self.fontFredokaOne)
        inkyphat.text((88, 64), "dimecoinnetwork.com", inkyphat.BLACK, font=self.fontFredokaOne)
        inkyphat.text((60, 90), "Starting up DimeTicker...", inkyphat.RED, font=self.fontFredokaOne)

        inkyphat.show()

    def donations(self, path):
        inkyphat.rectangle([(0, 0), (212, 104)], fill=inkyphat.WHITE, outline=None)  # Clear Screen
        donations = Image.open(path)
        inkyphat.paste(donations, (1, 1))
        inkyphat.text((5, 64), "DIME", inkyphat.BLACK, font=self.fontPressStart2P)
        inkyphat.text((93, 64), "BTC", inkyphat.BLACK, font=self.fontPressStart2P)
        inkyphat.text((169, 64), "ETH", inkyphat.BLACK, font=self.fontPressStart2P)
        inkyphat.text((5, 77), "Donations welcome!", inkyphat.BLACK, font=self.fontFredokaOne)
        inkyphat.text((5, 90), "Thank you for using DimeTicker!", inkyphat.RED, font=self.fontFredokaOne)

        inkyphat.show()

if __name__ == '__main__':
    dt = DimeTicker()
    c_len = len(dt.coinList)

    dt.splashScreen("./img/dimeNetworkqr_small.png")
    time.sleep(5)
    try:
        while True:
            #for each coin in coinlist, set logo and text, run the API, display everything, then sleep

            #dt.setQR("./img/DIMEdonationqr.png")
            for i in range(c_len):
                dt.setLogo("./img/" + dt.coinList[i] + ".png",dt.coinList[i], dt.currencyList[0])
                inkyphat.rectangle([(57, 1), (210, 23)], fill=inkyphat.WHITE, outline=None) # Clear the title bar
                title = str(datetime.datetime.now())
                inkyphat.text((60, 3), title, inkyphat.BLACK, font=dt.fontFredokaOne)
                try:
                    price, hr_change = dt.getPrice(dt.coinList[i], dt.currencyList[0])
                except: 
                    price = 0
                    hr_change = 0
                    pass

                print(f"{dt.coinList[i]} price: {price} {dt.currencyList[0]}")
                print(f"Percent Change in the last hour: {hr_change}%")
                dt.displayPrice(str(price), str(hr_change))
                inkyphat.show()
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
        dt.donations("./img/donations.png")
        sys.exit()

