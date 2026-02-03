def postal_check(postal):
    if len(postal) != 6:
        raise ValueError("Length of postal code is incorrect! It should be exactly 6 digits.")
    if not postal.isdigit():
        raise ValueError("Postal code should contain only digits, with no letters, spaces, or special characters.")
    return True

