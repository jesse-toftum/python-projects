"""
One Away: There are three types of edits that can be performed on strings:
insert a character, remove a character, or replace a character. Given two
strings, write a function to check if they are one edit (or zero edits) away.
"""


def one_away_replace(first: str, second: str) -> bool:
    """
    Checks whether a string can be reached by replacing a single character.

    Parameters
    ----------
    first : str
        The first string
    second : str
        The second string

    Returns
    -------
    bool
        True if the `first` can be transformed into `second` with one
        replacement
    """
    # This is used to check whether a change has already been made
    change_found = False

    # Iterate over both strings and check whether changes line up
    for i, j in zip(first, second):
        if i != j:

            # It's fine if one change was found, but not more than one
            if change_found:
                return False

            # Since a change was definitely found, update change_found
            change_found = True

    # Made it to the end of the loop, so first
    # must be within one replacement of second
    return True


def one_away_insert(first: str, second: str) -> bool:
    """
    Checks whether a string can be reached by inserting a single character.

    Parameters
    ----------
    first : str
        The first string
    second : str
        The second string

    Returns
    -------
    bool
        True if the `first` can be transformed into `second` with one insertion
    """
    # This is used to check whether a change has already been made
    change_found = False

    # Iterate over both strings and check whether changes line up
    i, j = 0, 0
    while i < len(first) and j < len(second):
        if first[i] != second[j]:
            if change_found:
                return False
            change_found = True
            j += 1
        else:
            i += 1
            j += 1
    return True


def one_away(first: str, second: str) -> bool:
    """
    Checks whether a string is within one edit of another

    Parameters
    ----------
    first : str
        The first string
    second : str
        The second string

    Returns
    -------
    bool
        True if the `first` can be transformed into `second` with one edit
    """
    if len(first) == len(second):
        return one_away_replace(first, second)
    if len(first) + 1 == len(second):
        return one_away_insert(first, second)
    if len(first) - 1 == len(second):
        return one_away_insert(second, first)
    return False


print(f"pale,  ple  -> {one_away('pale', 'ple')}")
print(f"pales, pale -> {one_away('pales', 'pale')}")
print(f"pale,  bale -> {one_away('pale', 'bale')}")
print(f"pale,  bake -> {one_away('pale', 'bake')}")
