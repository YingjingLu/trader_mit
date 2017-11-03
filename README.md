Env:
Developed in python 3.5
Downward compatible with python 2.7

Further development should mind python2 compatibility:
    - int float division
    - print statement
---------------------------------------------------------------


File Specs:

main.py

initialize the traders bot with given username password and ip
run the bot

-----------------------------------------------------------

src.gb.py

global variables of algorithms and mult variables

-----------------------------------------------------------

src.options_bot.py

wrapping class of the traders bot with all the callbacks

-----------------------------------------------------------

src.options_algo.py

static methods for option pricing calculation

------------------------------------------------------------


To run the program:

1. adjust the type of bot to run in main()
2. adjust the ip, username, password

terminal:
python -i main.py

