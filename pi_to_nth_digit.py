"""
Calculates Pi with some fun math
"""
import time
from decimal import Decimal as Dec
from decimal import getcontext as gc


# noinspection SpellCheckingInspection
def chudnovsky(precision, max_iter=100, timeout=False):
    """
    
    Calculates pi using the Chudnovsky algorithm:
    https://en.wikipedia.org/wiki/Chudnovsky_algorithm

    Runs in O(n log(n)^3).
    
    :param precision: The level of precision to be used
    :param max_iter: The maximum number of iterations to be used
    :param timeout: The maximum number of seconds to pass before refusing to continue summation.
    Note that this can potentially drastically affect the accuracy of the calculation.
    :return: Pi to some level of precision
    """
    gc().prec = precision + 1
    k_term = 6
    multinomial_term = 1
    linear_term = 13591409
    exponential_term = 1
    current_sum = 13591409
    start = time.time()
    for k in range(1, max_iter + 1):
        if timeout and time.time() > start + timeout:
            break
        multinomial_term = (k_term**3 - 16 * k_term) * multinomial_term // k**3
        linear_term += 545140134
        exponential_term *= -262537412640768000
        current_sum += Dec(multinomial_term * linear_term) / exponential_term
        k_term += 12
    c_term = 426880 * Dec(10005).sqrt()
    pi = c_term / current_sum
    pi = Dec(str(pi)[:precision])  # Only return up to the level of precision
    return pi


print(chudnovsky(10000, max_iter=500))
