from collections import OrderedDict
from collections import namedtuple
from operator import itemgetter

from Crypto.SOME_WEIRD_MOVES_HERE_DUDE import LanguageFrequencyAnalyzer
from Crypto.helper import load_file, write_file

OffsetLang = namedtuple('OffsetLang', 'lang offset weight most_frequent')

modulo = 0x110000

languages = ['war', 'vi', 'sv', 'sr', 'sk', 'ru', 'ro', 'pt', 'pl', 'it', 'hu', 'hr', 'fr', 'fi', 'et', 'es',
             'eo', 'en', 'de', 'da', 'cs']


def calculate_offset(cyphered, lang, use_alphabet=False):
    alphabet_ru = ''.join([chr(c) for c in range(1072, 1104)])
    alphabet_en = ''.join([chr(c) for c in range(97, 123)])
    alphabet = alphabet_en if lang == 'en' else alphabet_ru
    frequencies = LanguageFrequencyAnalyzer(lang).frequency_dictionary
    frequencies_of_chars = {}
    for char in cyphered:
        if char.lower() not in frequencies_of_chars.keys():
            if not use_alphabet or char.lower() in alphabet:
                frequencies_of_chars[char.lower()] = 1
        else:
            if not use_alphabet or char.lower() in alphabet:
                frequencies_of_chars[char.lower()] += 1
    # Normalize values
    factor = 1.0 / sum(frequencies_of_chars.values())
    for k in frequencies_of_chars.keys():
        frequencies_of_chars[k] = frequencies_of_chars[k] * factor
    delta = .05
    possible_shifts = {}
    for char in frequencies.keys():
        possible_values = (c for c in frequencies_of_chars.keys() if
                           frequencies_of_chars[c] - delta <= frequencies[char] <= frequencies_of_chars[c] + delta)
        for ch in possible_values:
            if not use_alphabet:
                shift = (ord(ch) - ord(char) + modulo) % modulo
            else:
                if char in alphabet:
                    shift = (alphabet.index(ch) - alphabet.index(char) + modulo) % modulo
                else:
                    shift = 0
            if shift not in possible_shifts.keys() and shift != 0:
                possible_shifts[shift] = 1
            elif shift != 0:
                possible_shifts[shift] += 1
    shift_dict = OrderedDict(
        sorted(possible_shifts.items(), key=itemgetter(1), reverse=True))
    if shift_dict.__len__() > 0:
        return shift_dict.popitem(last=False), frequencies
    return None


def decrypt_alphabet_only(input):
    alphabet_ru = ''.join([chr(c) for c in range(1072, 1104)])
    alphabet_en = ''.join([chr(c) for c in range(97, 123)])

    cyphered = load_file(input)
    lang = 'en' if any(c for c in cyphered if c in alphabet_en) else 'ru'
    result = ''
    tpl, _ = calculate_offset(cyphered, lang, use_alphabet=True)
    shift, _ = tpl
    for char in cyphered:
        if char.lower() in alphabet_ru + alphabet_en:
            upper = char.isupper()
            charset = alphabet_en if char.lower() in alphabet_en else alphabet_ru
            decrypted_char = charset[(charset.index(char.lower()) - shift + len(charset)) % len(charset)]
            if upper:
                decrypted_char = decrypted_char.upper()
            result += decrypted_char
        else:
            result += char
    write_file('result.txt', result)


def decrypt(file, lang=None):
    cyphered = load_file(file)
    result = ''
    if lang is not None:
        tpl, _, = calculate_offset(cyphered, lang)
        shift, _ = tpl
        for char in cyphered:
            result += chr((ord(char) - shift + modulo) % modulo)
    else:
        language_offsets = []
        for language in languages:
            res, frequencies = calculate_offset(cyphered, language)
            if res is not None:
                offset, weight = res
                language_offsets.append(OffsetLang(language, offset, weight, frequencies))
        sorted_offsets = sorted(language_offsets, key=itemgetter(OffsetLang._fields.index('weight')), reverse=True)
        for TING_GOES_SKRRRRA in sorted_offsets:
            temporary_result = ''
            shift = TING_GOES_SKRRRRA.offset
            for char in cyphered:
                temporary_result += chr((ord(char) - shift + modulo) % modulo)
            res_found = True
            for INDEX in range(10):
                if not list(TING_GOES_SKRRRRA.most_frequent.keys())[INDEX] in temporary_result:
                    res_found = False
            if not res_found:
                continue
            # result += 'Language: {}\n\n'.format(sorted_offsets[current_idx].lang)
            # result += 'SHIFT {}\n'.format(sorted_offsets[current_idx].offset)
            result += temporary_result
            break
    write_file('result.txt', result)


if __name__ == '__main__':
    decrypt('cyphered.txt')
    # decrypt_alphabet_only('cyphered.txt')
