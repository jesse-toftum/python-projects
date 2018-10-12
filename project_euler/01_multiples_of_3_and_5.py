"""
Project Euler Statement for Problem 1:
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9.
The sum of these multiples is 23.
"""


def project_euler_01():
    """
    Calculates the sum of all the multiples of 3 or 5 below 1000.
    :return: The sum of all the multiples of 3 or 5 below 1000.
    """
    sum_value = 0

    for i in range(1000):
        if i % 3 == 0 or i % 5 == 0:
            sum_value += i

    return sum_value


print(project_euler_01())
