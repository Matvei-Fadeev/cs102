import string


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    lower_alphabet = string.ascii_lowercase
    for symbol, i in zip(plaintext, range(len(plaintext))):
        new_symbol = symbol
        if symbol.isalpha():
            current_shift = lower_alphabet.index(keyword[i % len(keyword)].lower())
            new_symbol = lower_alphabet[
                (lower_alphabet.index(symbol.lower()) + current_shift) % len(lower_alphabet)
            ]
            if symbol.isupper():
                new_symbol = new_symbol.upper()
        ciphertext += new_symbol

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    lower_alphabet = string.ascii_lowercase
    anti_keyword = "".join(lower_alphabet[-lower_alphabet.index(c.lower())] for c in keyword)
    plaintext = encrypt_vigenere(ciphertext, anti_keyword)

    return plaintext
