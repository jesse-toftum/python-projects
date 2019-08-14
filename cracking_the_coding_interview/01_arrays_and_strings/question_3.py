"""
URLify: Write a method to replace all spaces in the string with `%20`. You may
assume that the string has sufficient space at the end to hold the additional
characters, and that you are given the "true" length of the string. (Note: if
implementing in Java, please use a character array so that you can perform this
operation in place.)
"""


def urlify(string: str, length: int) -> str:
    """
    Replaces the spaces in a given string with `%20`.

    Parameters
    ----------
    string : str
        The string to replace spaces in
    length : int
        The "true" length of the string

    Returns
    -------
    str
        A string where spaces are replaced with `%20`.
    """
    # This is a list of strings to allow for efficient concatenation
    url = []
    for i in range(length):
        if string[i] == ' ':
            url.append('%20')
        else:
            url.append(string[i])
    return ''.join(url)


print('"' + urlify("Mr John Smith", 13) + '"')
