

'''
{
    'ticker': 'T90P',
    'last_price': 87,
    'top_bid': 89,
    'low_ask': 78,
    'elapse': 3

}
'''
def mkt_update_parser(msg):
    res = dict()
    mkt_state = msg['market_state']

    ticker = mkt_state['ticker']
    last_price = float(mkt_state['last_price'])

    bid_list = list()
    for price, amt in mkt_state['bids'].items():
        bid_list.append((float(price), amt))
    bid_list.sort(key = lambda x: x[0])

    ask_list = list()
    for price, amt in mkt_state['asks'].items():
        ask_list.append((float(price), amt))
    ask_list.sort(key = lambda x: x[0])

    res['ticker'] = ticker
    res['last_price'] = last_price
    res['top_bid'] = bid_list[-1][0] if bid_list != [] else-1.0
    res['low_ask'] = ask_list[0][0] if ask_list != [] else-1.0
    res['elapse'] = msg['elapsed_time']
    print(res)
    assert(type(res['top_bid']) == float and type(res['low_ask']) == float)
    return res
'''
{
    'ticker':{
                'price': 90,
                'quantity': +- 30
            },
    'ticker': {
                csvsvsd
    }
}
'''
def on_trade_parser(msg):
    res = dict()
    for trade_dict in msg['trades']:
        ticker = trade_dict['ticker']
        buy = trade_dict['buy']
        price = trade_dict['price']
        if buy:
            quantity = trade_dict['quantity']
        else:
            quantity = -1*trade_dict['quantity']
        res[ticker] = {'price': price, 'quantity': quantity}
    return res

'''
{
    "message_type": "ACK MODIFY ORDERS",
    "cancels": {
        "AAPL:8349": None
    },
    "orders": [
        {
            "order_id": "AAPL:900o",
            "ticker": "AAPL",
            "buy": True,
            "quantity": 100,
            "price": 99.74,
            "token": "sqv6ajor"
        },
        # more order {...} of the same type
    ],
    "token": "ze12a9k9"
}
'''

def modify_order_parser(msg):
    order_list = []
    if 'orders' in msg:
        for order_dict in msg['orders']:
            buy = 1 if order_dict['buy'] == True else -1
            pos = order_dict['quantity'] * buy
            ticker = order_dict['ticker']
            price = order_dict['price']
            order_list.append({'pos': pos, 'ticker': ticker, 'price': price, 'highest': price})
    return order_list
