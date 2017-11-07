from tradersbot import TradersBot, TradersOrder
from gb import *
from msg_parser import *
from options_algo import *

class OptionsBot(object):

    def __init__(self, ip, username = 'trader0', password = 'trader0'):
        self.ip = ip
        self.ticker = 0
        self.username = username
        self.password = password
        self.traders_bot = TradersBot(self.ip, self.username, self.password)
        self.order = TradersOrder()
        self.set_callbacks()

    # ------------------------- Callbacks --------------------------#
    # need to adjust this part since trader actions are also executed in callbacks
    
    # update mkt info in everytime there is an update
    # arrive every 0.5 sec
    def onMarketUpdate_Wrapper(self, msg, traders_order):
        # print("--- in onMarketUpdateWrapper")
        # print("msg: ", msg)
        # print('traders_order', traders_order)
        res_dict = mkt_update_parser(msg)
        update_msg_pos(res_dict)

        # clear positions
        # ticker, amount, buy/sell
        res_tuple = clear_msg_pos(res_dict)
        if res_tuple != tuple():
            ticker, amt, act = res_tuple
            if act == 'buy':
                traders_order.addBuy(ticker, amt)
                record_order(ticker, amt, CUR_PRICE_DICT[ticker]['low_ask'], traders_order)
            elif act == 'sell':
                traders_order.addSell(ticker, amt)
                record_order(ticker, -1*amt, CUR_PRICE_DICT[ticker]['top_bid'], traders_order)
        # seek arbitrage
        res_list = calc_arbitrage_in_diff_k(res_dict)
        if res_list != []:
            res_list = res_list[0]
            traders_order.addBuy(res_list[0], res_list[1])
            record_order(res_list[0], res_list[1], CUR_PRICE_DICT[res_list[0]]['low_ask'], traders_order)
            traders_order.addSell(res_list[2], res_list[3])
            record_order(res_list[0], -1*res_list[1], CUR_PRICE_DICT[res_list[0]]['top_bid'], traders_order)

        return (msg, traders_order)

    # reports account info. We should also track the account internally
    # arrive every 0.5 sec
    def onTraderUpdate_Wrapper(self, msg, traders_order):
        # print("--- in onTraderUpdate_Wrapper")
        # print("msg: ", msg)
        # print('traders_order', traders_order)
        

        return (msg, traders_order)

    # arrive when an internal or external trade take place
    def onTrade_Wrapper(self, msg, traders_order):
        # print("--- in onTrade_Wrapper")
        # print("msg: ", msg)
        # print('traders_order', traders_order)
        return (msg, traders_order)

    # called on connect to verify connections
    def onAckRegister_Wrapper(self, msg, traders_order):
        # print("--- in onAckRegister_Wrapper")
        # print("msg: ", msg)
        # print('traders_order', traders_order)
        return (msg, traders_order)

    # called when server recognize a order or order update
    def onAckModifyOrders_Wrapper(self, msg, traders_order):
        # print("--- in onAckModifyOrders_Wrapper")
        # print("msg: ", msg)
        # print('traders_order', traders_order)
        order_list = modify_order_parser(msg)
        for order_dict in order_list:
            ticker = order_dict['ticker']
            if CUR_POS_DICT.get(ticker) == None:
                CUR_POS_DICT[ticker] = order_dict
            else:
                CUR_POS_DICT[ticker]['pos'] += order_dict['pos']
                if CUR_POS_DICT[ticker]['pos'] == 0:
                    del CUR_POS_DICT[ticker]
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


