"""
Project Euler Statement for Problem 3:

The prime factors of 13195 are 5, 7, 13 and 29.
What is the largest prime factor of the number 600851475143 ?
"""
from math import ceil, sqrt
from typing import Set, List, Union


def prime_factors(number: int, full=True):
    """
    Calculates and returns the prime factors of a number

    Parameters
    ----------
    number : int
        The number to find the prime factors of
    full : bool, optional
        Whether to find the full prime factorization of the number.
        If this is True, it will return a list. If False, it will return a set.
        By default True.

    Returns
    -------
        A list or set of prime factors of number
    """
    found_primes = []
    original_number = number
    while number % 2 == 0:
        found_primes.append(2)
        number /= 2

    for i in range(3, ceil(sqrt(original_number)) + 2, 2):
        while number % i == 0:
            found_primes.append(i)
            number /= i
    return found_primes if full else set(found_primes)


print(prime_factors(600851475143)[-1])
