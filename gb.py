# global variables in this file
# all other files should include this 
CALL_STRIKE_DICT = {
    'T80C':80,
    'T81C':81,
    'T82C':82,
    'T83C':83,
    'T84C':84,
    'T85C':85,
    'T86C':86,
    'T87C':87,
    'T88C':88,
    'T89C':89,

    'T90C':90,
    'T91C':91,
    'T92C':92,
    'T93C':93,
    'T94C':94,
    'T95C':95,
    'T96C':96,
    'T97C':97,
    'T98C':98,
    'T99C':99,

    'T100C':100,
    'T101C':101,
    'T102C':102,
    'T103C':103,
    'T104C':104,
    'T105C':105,
    'T106C':106,
    'T107C':107,
    'T108C':108,
    'T109C':109,

    'T110C':110,
    'T111C':111,
    'T112C':112,
    'T113C':113,
    'T114C':114,
    'T115C':115,
    'T116C':116,
    'T117C':117,
    'T118C':118,
    'T119C':119,

    'T120C':120,
}

PUT_STRIKE_DICT = {
    'T80P':80,
    'T81P':81,
    'T82P':82,
    'T83P':83,
    'T84P':84,
    'T85P':85,
    'T86P':86,
    'T87P':87,
    'T88P':88,
    'T89P':89,

    'T90P':90,
    'T91P':91,
    'T92P':92,
    'T93P':93,
    'T94P':94,
    'T95P':95,
    'T96P':96,
    'T97P':97,
    'T98P':98,
    'T99P':99,

    'T100P':100,
    'T101P':101,
    'T102P':102,
    'T103P':103,
    'T104P':104,
    'T105P':105,
    'T106P':106,
    'T107P':107,
    'T108P':108,
    'T109P':109,

    'T110P':110,
    'T111P':111,
    'T112P':112,
    'T113P':113,
    'T114P':114,
    'T115P':115,
    'T116P':116,
    'T117P':117,
    'T118P':118,
    'T119P':119,
    
    'T120P':120,
}

STRIKE_OPTION_DICT = {
    90: ('T90P', 'T90C'),
    95: ('T95P', 'T95C'),
    100: ('T100P', 'T100C'),
    105: ('T105P', 'T105C'),
    110: ('T110P', 'T110C')
}
# 'T90P': {'last_price': -1, 'low_ask': 1.98, 'top_bid': 90}
CUR_PRICE_DICT = dict()

# 'T90P': {'pos': -100, 'price': 1.98, 'highest': 1.98}
CUR_POS_DICT = dict()


PUT_NUM = 10
CALL_NUM = 10

# _____________ GBs in black sholes methods ____________#
#_______________ options_traders.py _______________-____#
PDF_MU = 0.0
PDF_SIGMA = 1.0


tic = 0
# number if contract execute every time
NUM_CONTRACT = 10

# _____________ End GBs in black sholes methods ____________#
OPTION_LEFT = 5000

# stopping threshold, in prcentages
GAIN_STOP_FROM_HIGH = 0.01
LOSS_STOP = 0.01
CONTRACT_COST = 0.01

CALC_ARB_DIFF_CAALL_THRESH = 0.05

HOLDING_LIMIT = 300