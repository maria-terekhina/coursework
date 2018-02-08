import re
from translator import Translator
from pl_stemmer import PlStammer
from nltk.stem import SnowballStemmer

class DictionaryKwic(object):
    def __init__(self, query, language, targetLanguage):
        self.query = query
        t = Translator(language + '-' + targetLanguage)  # в параллельных нужно задавать язык где-то изачально
        self.translations = t.translate(query)
        self.stemmer = self.choose_stemmer(targetLanguage)

    def choose_stemmer(self, targetLanguage):
        if targetLanguage == 'pl':
            return PlStammer()
        if targetLanguage in ['en']:
            return SnowballStemmer(targetLanguage)


    def results_to_kwic(self, results):
        stemmer = self.stemmer
        left_list = []
        center_list = []
        right_list = []
        others = []
        for pair in results:
            i = 0
            for word in self.translations:
                res = re.search(stemmer.stem(word) + '.+?\W', pair[1])
                if res is not None:
                    w = res.group(0)
                    print(w)
                    left_list.append([pair[0].split(self.query)[0], pair[1].split(w)[0]])
                    right_list.append([pair[0].split(self.query)[1], pair[1].split(w)[1]])
                    center_list.append([self.query, w])
                    i = 1
                    break

            if i is 0:
                others.append(pair)

        s = [[left_list[i], center_list[i], right_list[i]] for i in range(len(left_list))]

        return s, others