"""
Is Unique: Implement an algorithm to determine if a string has all unique
characters. What if you cannot use additional data structures?
"""


def is_unique(string: str) -> bool:
    """
    Checks whether a string is made of all unique characters.
    :param string: The string to check for uniqueness
    :return: True if the string is made of unique characters, and false
        if it is not.
    """
    return len(set(string)) == len(string)


def is_unique_2(string: str) -> bool:
    """
    Checks whether a string is made of all unique characters.
    This version uses sorting, and should run in O(n log(n)) time
    :param string: The string to check for uniqueness
    :return: True if the string is made of unique characters, and false
        if it is not.
    """
    sorted_string = sorted(string)
    for i in range(len(sorted_string) - 1):
        if sorted_string[i] == sorted_string[i + 1]:
            return False
    return True


def is_unique_3(string: str) -> bool:
    """
    Checks whether a string is made of all unique characters.
    This version also is much slower (that is, O(n^2)), as it compares every
    character against every other character.
    :param string: The string to check for uniqueness
    :return: True if the string is made of unique characters, and false
        if it is not.
    """
    for i in range(len(string)):
        for j in range(i + 1, len(string)):
            if string[i] == string[j]:
                return False
    return True
