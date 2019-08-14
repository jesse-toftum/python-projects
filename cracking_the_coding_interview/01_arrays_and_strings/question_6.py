"""
String Compression: Implement a method to perform basic string compression using
the counts of repeated characters. For example, the string `aabcccccaaa` would
become `a2b1c5a3`. If the "compressed" string would not become smaller than the
original string, your method should return the original string. You can assume
the string has only uppercase and lowercase letters (a - z).
"""
import numpy as np


def string_compression(string: str) -> str:
    """
    Performs basic string compression using the counts of repeated characters.
    If the "compressed" string would not be smaller than the original, returns
    the original string instead.

    Parameters
    ----------
    string : str
        The string to attempt to compress

    Returns
    -------
    str
        The potentially compressed string, or the original string if the
        "compressed" version would not be shorter.
    """
    # Appending to a list can potentially be more efficient than appending to
    # the string, resulting in runtime of O(n) rather than O(n^2)
    compressed_list = []

    # Keeps track of the number of consecutive letters
    consecutive = 0

    # Loop over the string, keeping track of both index and character at index
    for index, character in enumerate(string):

        # Increase the count of consecutive letters until the letter changes
        consecutive += 1

        # Once the letter changes (or we've reached the end of the string)
        if index + 1 >= len(string) or character != string[index + 1]:

            # Add the character and count to the compressed list
            compressed_list.append(character)
            compressed_list.append(str(consecutive))

            # Reset count back to zero
            consecutive = 0

    # Join the contents of the list together and return
    return ''.join(compressed_list)


print(f"aabcccccaaa -> {string_compression('aabcccccaaa')}")
