"""
Check Permutation: Given two strings, write a method to decide if one is a
permutation of the other.
"""


def check_permutation(string_1: str, string_2: str) -> bool:
    """
    Checks whether one string is a permutation of the other.

    Parameters
    ----------
    string_1 : str
        Some string
    string_2 : str
        Another string

    Returns
    -------
    bool
        True if one string is a permutation of another.
    """
    if len(string_1) != len(string_2):
        return False
    return sorted(string_1) == sorted(string_2)
