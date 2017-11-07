# trading algo functions for options 
# all in static method format

from gb import *
import math


class OptionsAlgo:


    # _________________ Calc Black Schole ________________#
    '''
    Return the value of the Gaussian probability function with mean 0.0
    and standard deviation 1.0 at the given x value.
    '''
    @staticmethod
    def phi(x):
        return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)

    # Return the value of the Gaussian probability function with mean mu
    # and standard deviation sigma at the given x value.
    @staticmethod
    def pdf(x, mu = PDF_MU, sigma = PDF_SIGMA):
        return OptionsAlgo.phi((x - mu) / sigma) / sigma


    # Return the value of the cumulative Gaussian distribution function
    # with mean 0.0 and standard deviation 1.0 at the given z value.
    def cumulative_gaussian(z):
        if z < -8.0: return 0.0
        if z >  8.0: return 1.0
        total = 0.0
        term = z
        i = 3
        while total != total + term:
            total += term
            term *= z * z / float(i)
            i += 2
        return 0.5 + total * OptionsAlgo.phi(z)

    # Return standard Gaussian cdf with mean mu and stddev sigma.
    # Use Taylor approximation.

    def cdf(z, mu = PDF_MU, sigma = PDF_SIGMA):
        return OptionsAlgo.cumulative_gaussian((z - mu) / sigma)

    # Black-Scholes formula.
    def BS_callPrice(s, x, r, sigma, t):
        a = (math.log(s/x) + (r + sigma * sigma/2.0) * t) / \
            (sigma * math.sqrt(t))
        b = a - sigma * math.sqrt(t)
        return s * OptionsAlgo.cdf(a) - x * math.exp(-r * t) * cdf(b)

    # _____________End Calc Black Schole ________________#


# _______________ Identifying put call parity opportunities _________#


# _______ Algo for put call arbutrage among different strike price _________#

def update_msg_pos(res_dict):
    ticker = res_dict['ticker']
    price = res_dict['last_price']
    bid = res_dict['top_bid']
    ask = res_dict['low_ask']
    elapse = res_dict['elapse']

    # update CUR_PRICE DICT
    CUR_PRICE_DICT[ticker] = {'last_price': price, 'low_ask': ask, 'top_bid': bid}
    # update CUR_POS_DICT, ON peak for both positive and negative pos
    if CUR_POS_DICT.get(ticker) != None:
        if CUR_POS_DICT[ticker]['pos'] < 0:
            CUR_POS_DICT[ticker]['highest'] = min(CUR_POS_DICT[ticker]['highest'], price)
        else:
            CUR_POS_DICT[ticker]['highest'] = max(CUR_POS_DICT[ticker]['highest'], price)

def calc_arbitrage_in_diff_k(res_dict):
    this_ticker = res_dict['ticker']
    this_price = res_dict['last_price']
    this_bid = res_dict['top_bid']
    this_ask = res_dict['low_ask']

    # [buy-tick, buy-amt, sell-tick, sell-amt, diff]
    diff_index = 4
    buy_sell_list = []
    # if call option

    if this_ticker in CALL_STRIKE_DICT:
        this_K = CALL_STRIKE_DICT[this_ticker]

        for other_ticker in CALL_STRIKE_DICT:
            if other_ticker in CALL_STRIKE_DICT and other_ticker in CUR_PRICE_DICT:
                other_K = CALL_STRIKE_DICT[other_ticker]
                other_price = CUR_PRICE_DICT[other_ticker]['last_price']
                other_bid = CUR_PRICE_DICT[other_ticker]['top_bid']
                other_ask = CUR_PRICE_DICT[other_ticker]['low_ask']

                # if this is over prices, sell this and buy other
                # if (this_K + this_price) > (other_K + other_price) and :
                diff1 = (this_K + this_bid)  - (other_K + other_ask)
                diff2 = (other_K + other_bid) - (this_K + this_ask)
                if (diff1 > (2*CONTRACT_COST + CALC_ARB_DIFF_CAALL_THRESH)) and (this_K < other_K):

                    # sell this buy other
                    buy_sell_list.append([ 
                                            other_ticker,
                                            NUM_CONTRACT,
                                            this_ticker,
                                            NUM_CONTRACT,
                                            (diff1 - 2*CONTRACT_COST)*NUM_CONTRACT
                                         ])

                # if other is over prices, sell other and buy this
                elif (diff2 > (-2*CONTRACT_COST+CALC_ARB_DIFF_CAALL_THRESH)) and (this_K > other_K):
                    # sell other buy this
                    buy_sell_list.append([ 
                                            this_ticker,
                                            NUM_CONTRACT,
                                            other_ticker,
                                            NUM_CONTRACT,
                                            (diff2 - 2*CONTRACT_COST)*NUM_CONTRACT
                                         ])
    # if put option
    if this_ticker in PUT_STRIKE_DICT:
        this_K = PUT_STRIKE_DICT[this_ticker]
        for other_ticker in PUT_STRIKE_DICT:
            if other_ticker in PUT_STRIKE_DICT and other_ticker in CUR_PRICE_DICT:
                other_K = PUT_STRIKE_DICT[other_ticker]
                other_price = CUR_PRICE_DICT[other_ticker]['last_price']
                other_bid = CUR_PRICE_DICT[other_ticker]['top_bid']
                other_ask = CUR_PRICE_DICT[other_ticker]['low_ask']

                # if this is smaller sell this and buy other
                diff1 = other_K - other_ask - (this_K - this_bid)
                # if other is smaller, sell other buy this
                diff2 = (this_K - this_ask) - (other_K - other_bid)

                if (diff1 > (2*CONTRACT_COST + CALC_ARB_DIFF_CAALL_THRESH)) and (this_K > other_K):
                    buy_sell_list.append([ 
                                            other_ticker,
                                            NUM_CONTRACT,
                                            this_ticker,
                                            NUM_CONTRACT,
                                            (diff1 - 2*CONTRACT_COST)*NUM_CONTRACT
                                         ])

                elif (diff2 > (2*CONTRACT_COST + CALC_ARB_DIFF_CAALL_THRESH)) and (this_K < other_K):
                    buy_sell_list.append([ 
                                            this_ticker,
                                            NUM_CONTRACT,
                                            other_ticker,
                                            NUM_CONTRACT,
                                            (diff2 - 2*CONTRACT_COST)*NUM_CONTRACT
                                         ])

    if buy_sell_list != []:
        buy_sell_list.sort(key = lambda x: x[diff_index], reverse = True)
    return buy_sell_list




def clear_msg_pos(res_dict):
    ticker = res_dict['ticker']
    price = res_dict['last_price']
    bid = res_dict['top_bid']
    ask = res_dict['low_ask']
    elapse = res_dict['elapse']

    # ticker, amount, buy/sell
    res = []

    if CUR_POS_DICT.get(ticker) != None:
        print("Close Order", "Ticker: ", ticker, "Price: ", price, 'Sell')

        pos_dict = CUR_POS_DICT[ticker]
        # stop long pos
        if pos_dict['pos'] > 0:
            # stop loss
            if (pos_dict['price'] - price)/ pos_dict['price'] > LOSS_STOP:
                res = [ticker,pos_dict['pos'], 'sell']
            # stop gain
            elif (pos_dict['highest'] - price)/ pos_dict['price'] > GAIN_STOP_FROM_HIGH:
                res = [ticker,pos_dict['pos'], 'sell']



        # stop short position
        elif pos_dict['pos'] < 0:
            print("Close Order", "Ticker: ", ticker, "Price: ", price, 'Buy')
            # stop loss
            if(price - pos_dict['price']) / pos_dict['price'] > LOSS_STOP:
                res = [ticker, -1*pos_dict['pos'], 'buy']
            # stop gain
            elif (price - pos_dict['highest']) / pos_dict['price'] > GAIN_STOP_FROM_HIGH:
                res = [ticker, -1*pos_dict['pos'], 'buy']

    return tuple(res)

def record_order(ticker, pos, price, trade_order):
    if CUR_POS_DICT.get(ticker) != None:
        pos_dict = CUR_POS_DICT[ticker]
        if abs(pos_dict['pos'] + pos) < HOLDING_LIMIT:
            # print("Clear previous Position")
            # # if in short then buy back
            # if pos_dict['pos'] < 0:
            #     trade_order.addBuy(pos_dict[ticker], -1*pos_dict['pos'])
            #     del CUR_POS_DICT[ticker]
            # else:
            #     rade_order.addSell(pos_dict[ticker], pos_dict['pos'])
            #     del CUR_POS_DICT[ticker]

    


            if CUR_POS_DICT.get(ticker) != None:
                print("Order: ", ticker, "Pos", pos, 'Price: ', price)
                pos_dict = CUR_POS_DICT[ticker]
                if pos_dict['pos']+pos == 0:
                    del CUR_POS_DICT[ticker]
                    return
                price = (price*pos+pos_dict['price']*pos_dict['pos'])/(pos_dict['pos'] + pos)
                pos_dict['pos'] += pos
                pos_dict['price'] = price
                
            else:
                CUR_POS_DICT[ticker] = {'pos':pos, 'price':price, 'highest': price}
