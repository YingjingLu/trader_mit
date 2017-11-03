# trading algo functions for options 
# all in static method format

from src.gb import *
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