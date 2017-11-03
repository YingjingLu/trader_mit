from tradersbot import TradersBot 
from src.gb import *

class OptionsBot(object):

    def __init__(self, ip, username = 'trader0', password = 'trader0'):
        self.ip = ip
        self.username = username
        self.password = password
        self.traders_bot = TradersBot(self.ip, self.username, self.password)
        self.set_callbacks()

    # ------------------------- Callbacks --------------------------#
    # need to adjust this part since trader actions are also executed in callbacks
    
    # update mkt info in everytime there is an update
    # arrive every 0.5 sec
    def onMarketUpdate_Wrapper(self, msg, traders_order):
        print("--- in onMarketUpdateWrapper")
        print("msg: ", msg)
        print('traders_order', traders_order)
        return (msg, traders_order)

    # reports account info. We should also track the account internally
    # arrive every 0.5 sec
    def onTraderUpdate_Wrapper(self, msg, traders_order):
        print("--- in onTraderUpdate_Wrapper")
        print("msg: ", msg)
        print('traders_order', traders_order)
        return (msg, traders_order)

    # arrive when an internal or external trade take place
    def onTrade_Wrapper(self, msg, traders_order):
        print("--- in onTrade_Wrapper")
        print("msg: ", msg)
        print('traders_order', traders_order)
        return (msg, traders_order)

    # called on connect to verify connections
    def onAckRegister_Wrapper(self, msg, traders_order):
        print("--- in onAckRegister_Wrapper")
        print("msg: ", msg)
        print('traders_order', traders_order)
        return (msg, traders_order)

    # called when server recognize a order or order update
    def onAckModifyOrders_Wrapper(self, msg, traders_order):
        print("--- in onAckModifyOrders_Wrapper")
        print("msg: ", msg)
        print('traders_order', traders_order)
        return (msg, traders_order)


    # add basic callbacks to the traderbot
    def set_callbacks(self):
        self.traders_bot.onMarketUpdate = self.onMarketUpdate_Wrapper
        self.traders_bot.onTraderUpdate = self.onTraderUpdate_Wrapper
        self.traders_bot.onTrade = self.onTrade_Wrapper
        self.traders_bot.onAckRegister = self.onAckRegister_Wrapper
        self.traders_bot.onAckModifyOrders = self.onAckModifyOrders_Wrapper

        print("--- Basic callbacks setup Successfully")

    # ------------------------- Callbacks End --------------------------#


