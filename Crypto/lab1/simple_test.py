import sys

import requests

from Crypto.lab1 import helper, encryptor, decryptor

languages = ['war', 'vi', 'sv', 'sr', 'sk', 'ru', 'ro', 'pt', 'pl', 'it', 'hu', 'hr', 'fr', 'fi', 'et', 'es',
             'eo', 'en', 'de', 'da', 'cs']

if __name__ == '__main__':
    percentage_of_failed_tests = []
    lowest_border = 150
    result_achieved = False
    failed_languages = []
    lowest_border += 1
    for lang in languages:
        sys.stdout.write(
            '\r{percentage:02f}% passed.'.format(percentage=float(languages.index(lang)) / len(languages) * 100))
        sys.stdout.flush()
        test_text_found = False
        while not test_text_found:
            try:
                response = requests.get(
                    'https://{}.wikipedia.org/w/api.php'.format(lang),
                    params={
                        'action': 'query',
                        'format': 'json',
                        'generator': 'random',
                        'prop': 'extracts',
                        'exintro': True,
                        'explaintext': True}).json()
                page = next(iter(response['query']['pages'].values()))
                if 'extract' in page.keys():
                    source = page['extract']
                    if len(source) > lowest_border:
                        test_text_found = True
                if not test_text_found:
                    continue
                helper.write_file('plain.txt', source)
                expected_result = helper.load_file('plain.txt')
                encryptor.encrypt('plain.txt')
                decryptor.decrypt('cyphered.txt')
                original_result = helper.load_file('result.txt')
                assert expected_result == original_result
            except Exception as e:
                if not lang in failed_languages:
                    failed_languages.append(lang)
    failed_string = ' '.join(failed_languages)
    print()
    print('Border: {}'.format(lowest_border))
    print('Successfully passed {:02f}% of tests. Failed for {}'.format(
        float((len(languages) - len(failed_languages)) / len(languages) * 100),
        failed_string))
    if len(failed_languages) == 0:
        result_achieved = True
