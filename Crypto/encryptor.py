import random

from Crypto.helper import load_file, write_file

_MODULO = 0x110000


def encrypt(file):
    key = random.randrange(_MODULO)
    plaintext = load_file(file)
    cyphered = ''
    for char in plaintext:
        cyphered += chr((ord(char) + key) % _MODULO)
    write_file('cyphered.txt', cyphered)


def encrypt_using_alphabeet(input, lang):
    if lang == 'ru':
        alphabet = ''.join([chr(c) for c in range(1072, 1104)])
    elif lang == 'en':
        alphabet = ''.join([chr(c) for c in range(97, 123)])
    else:
        raise Exception('Wrong language..')
    key = random.randrange(1, len(alphabet))
    plaintext = load_file(input)
    cyphered = ''
    for char in plaintext:
        is_upper = char.isupper()
        if char.lower() in alphabet:
            encoded_char = alphabet[(alphabet.index(char.lower()) + key) % len(alphabet)]
            if is_upper:
                encoded_char = encoded_char.upper()
            cyphered += encoded_char
        else:
            cyphered += char
    write_file('cyphered.txt', cyphered)


if __name__ == '__main__':
    encrypt('plain.txt')
    # encrypt_using_alphabeet('plain.txt', 'ru')
