# this program downwards compatible with python 2.7
# recommend run in python 3.5

from src.gb import *
from src.options_bot import *
import sys


def main():
    option_bot = OptionsBot(ip = 'localhost')
    option_bot.traders_bot.run()

if __name__ == "__main__":
    main()