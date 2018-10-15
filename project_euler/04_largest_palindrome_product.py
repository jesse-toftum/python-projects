"""
Project Euler Statement for Problem 4:

A palindromic number reads the same both ways.
The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 * 99.

Find the largest palindrome made from the product of two 3-digit numbers.
"""


def is_palindrome(number: int):
    """

    Determines whether a given number is a palindrome.

    :param number: Some number to check
    :return: True if number is a palindrome, and false otherwise.
    """
    number_string = str(number)

    return number_string == number_string[::-1]


def project_euler_04():
    """
    Finds the highest palindromic number made from the product of two 3-digit numbers
    :return: The largest palindromic number from two 3-digit numbers, which happens to be 906609.
    """
    highest_palindrome = 0
    for i in range(999, 99, -1):
        for j in range(999, i - 1, -1):
            product = i * j
            if product <= highest_palindrome:
                continue
            if is_palindrome(product):
                highest_palindrome = product
    return highest_palindrome


print(project_euler_04())
