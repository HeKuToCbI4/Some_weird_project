import os
import pickle
import sys
from collections import OrderedDict
from operator import itemgetter

import requests


class LanguageFrequencyAnalyzer:
    def __init__(self, language):
        self.frequency_dictionary = pickle.load(open('{}.txt'.format(language), 'rb')) if os.path.isfile(
            '{}.txt'.format(language)) else {}
        self._lang = language

    def learn(self, steps, source_file=None):
        for i in range(steps):
            try:
                percentage = float(i) / steps
                sys.stdout.write('\rProgress: {num:02f}%'.format(num=percentage * 100))
                sys.stdout.flush()
                temporary_dictionary = {}
                response = requests.get(
                    'https://{}.wikipedia.org/w/api.php'.format(self._lang),
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
                else:
                    source = []
                if source_file is not None:
                    source = open(source_file, encoding='utf-8').read()
                for ch in source:
                    if ch not in [' ', '\n']:
                        if ch not in temporary_dictionary.keys():
                            temporary_dictionary[ch] = 1
                        else:
                            temporary_dictionary[ch] += 1
                try:
                    factor = 1.0 / sum(temporary_dictionary.values())
                    for k in temporary_dictionary.keys():
                        temporary_dictionary[k] = temporary_dictionary[k] * factor
                    for k in temporary_dictionary.keys():
                        if k in self.frequency_dictionary.keys():
                            self.frequency_dictionary[k] = (self.frequency_dictionary[k] + temporary_dictionary[k]) / 2
                        else:
                            self.frequency_dictionary[k] = temporary_dictionary[k] / 2
                except:
                    pass
            except Exception as e:
                print('Failed. Saving results. {}'.format(e))
        self.frequency_dictionary = OrderedDict(
            sorted(self.frequency_dictionary.items(), key=itemgetter(1), reverse=True))
        self.frequency_dictionary = {k: self.frequency_dictionary[k] for k in
                                     list(self.frequency_dictionary.keys())[:20]}
        print(self.frequency_dictionary.__len__())
        print(self.frequency_dictionary)
        pickle.dump(self.frequency_dictionary, open('{}.txt'.format(self._lang), 'wb'))
        print()


if __name__ == '__main__':
    for lang in ['war', 'vi', 'sv', 'sr', 'sk', 'ru', 'ro', 'pt', 'pl', 'it', 'hu', 'hr', 'fr', 'fi', 'et', 'es',
                 'eo', 'en', 'de', 'da', 'cs']:
        print('Right now we are learning: ', lang)
        learner = LanguageFrequencyAnalyzer(lang)
        learner.learn(200)
