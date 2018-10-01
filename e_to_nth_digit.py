import time
from decimal import Decimal as Dec
from decimal import getcontext as gc
from math import factorial


def calculate_e(precision, max_iter=100, timeout=False):
    """
    Calculates e using an algorithm found here:
    https://en.wikipedia.org/wiki/List_of_representations_of_e

    Accurate to within 2 * 10^-12 after 5 iterations
    :param precision: The level of precision to be used
    :param max_iter: The maximum number of iterations to be used
    :param timeout: The maximum number of seconds to pass before refusing to continue summation. Note that this can
    potentially drastically affect the accuracy of the calculation.
    :return: Euler's number e to some level of precision
    """
    gc().prec = precision + 1
    current_sum = Dec(0)
    start = time.time()
    for k in range(0, max_iter + 1):
        if timeout and time.time() > start + timeout:
            break
        numerator = Dec((4 * k) + 3)
        denominator_left = Dec(2 ** ((2 * k) + 1))
        denominator_right = factorial(Dec(2 * k + 1))
        current_term = Dec(numerator / (denominator_left * denominator_right))
        current_sum += current_term
    e = Dec(current_sum) ** 2
    e = Dec(str(e)[:precision])  # Only return up to the level of precision
    return e


print(calculate_e(10000, max_iter=500))
