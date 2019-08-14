"""
Palindrome Permutation: Given a string, write a function to check if it is a
permutation of a palindrome. A palindrome is a word or phrase that is the same
forwards and backwards. A permutation is a rearrangement of letters. The
palindrome does not need to be limited to just dictionary words.
"""


def palindrome_permutation(string: str) -> bool:
    """
    Checks whether a string can possibly be made into a palindrome. This is done
    by checking whether there is only one character in the string that shows up
    an odd number of times.

    Parameters
    ----------
    string : str
        The given string

    Returns
    -------
    bool
        True if the string can be made into a palindrome, otherwise False
    """
    lowercase = string.lower()
    # This could easily be a defaultdict from Collections
    letter_frequency = {}
    for i in lowercase:
        # Skip spaces, since they're irrelevant
        if i == " ":
            continue
        # If the letter hasn't shown up in letter_frequency, add it
        if i not in letter_frequency:
            letter_frequency[i] = 0
        # Either way, add 1 to the counted number
        letter_frequency[i] += 1

    number_of_odds = 0
    for count in letter_frequency.values():
        if count % 2 != 0:
            number_of_odds += 1

    # A palindrome can have at most one letter that shows
    # up an odd number of times, ignoring spaces
    return number_of_odds <= 1


print(palindrome_permutation("Tact Coa"))
