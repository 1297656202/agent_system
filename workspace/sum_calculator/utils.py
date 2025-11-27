import re


def validate_number(num_str):
    """
Validate if a string is a valid number (integer or float).

    Args:
        num_str (str): The string to validate

    Returns:
        bool: True if the string is a valid number, False otherwise
    """
    try:
        float(num_str)
        return True
    except ValueError:
        return False


def string_to_number(num_str):
    """
Convert a string to a number (int or float).

    Args:
        num_str (str): The string to convert

    Returns:
        float or int: The converted number value

    Raises:
        ValueError: If the string is not a valid number    
    """
    if '.' in num_str:
        return float(num_str)
    else:
        return int(num_str)


def calculate_sum(numbers):
    """
Calculate the sum of a list of numbers.

    Args:
        numbers (list): A list of numbers (int or float)

    Returns:
        float: The sum of all numbers in the list
    """
    return sum(numbers)