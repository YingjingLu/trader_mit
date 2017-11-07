from gb import *
from options_bot import *
import sys


def main():
    option_bot = OptionsBot(ip = 'localhost')
    option_bot.traders_bot.run()

if __name__ == "__main__":
    main()