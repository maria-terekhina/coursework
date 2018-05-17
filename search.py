from model import Model
from math import fabs
import urllib.request
import re

models = {'rus': 'russian-syntagrus-ud-2.0-170801.udpipe',
          'eng': 'english-ud-2.1-20180111.udpipe',
          'ita': 'italian-ud-2.0-170801.udpipe',
          'fra': 'french-sequoia-ud-2.1-20180111.udpipe',
          'ara': 'arabic-ud-2.0-170801.udpipe',
          'eus': 'basque-ud-2.0-170801.udpipe',
          'bel': 'belarusian-ud-2.0-170801.udpipe',
          'bul': 'bulgarian-ud-2.0-170801.udpipe',
          'cat': 'catalan-ud-2.0-170801.udpipe',
          'zho': 'chinese-ud-2.0-170801.udpipe',
          'cop': 'coptic-ud-2.0-170801.udpipe',
          'hrv': 'croatian-ud-2.0-170801.udpipe',
          'ces': 'czech-cltt-ud-2.0-170801.udpipe',
          'dan': 'danish-ud-2.0-170801.udpipe',
          'nld': 'dutch-ud-2.0-170801.udpipe',
          'est': 'estonian-ud-2.0-170801.udpipe',
          'fin': 'finnish-ud-2.0-170801.udpipe',
          'glg': 'galician-ud-2.0-170801.udpipe',
          'got': 'gothic-ud-2.0-170801.udpipe',
          'ell': 'greek-ud-2.0-170801.udpipe',
          'heb': 'hebrew-ud-2.0-170801.udpipe',
          'hin': 'hindi-ud-2.0-170801.udpipe',
          'hun': 'hungarian-ud-2.0-170801.udpipe',
          'ind': 'indonesian-ud-2.0-170801.udpipe',
          'gle': 'irish-ud-2.0-170801.udpipe',
          'jpn': 'japanese-ud-2.0-170801.udpipe',
          'kaz': 'kazakh-ud-2.0-170801.udpipe',
          'kor': 'korean-ud-2.0-170801.udpipe',
          'lat': 'latin-ud-2.0-170801.udpipe',
          'lav': 'latvian-ud-2.0-170801.udpipe',
          'lit': 'lithuanian-ud-2.0-170801.udpipe'}

class Aligner:
    '''
    Find translation of a query in a parallel text.
    '''

    def __init__(self, queryLanguage, targetLanguage):
        self.ql = queryLanguage
        self.tl = targetLanguage

        # download models if absent
        try:
            self.model_ql = Model(models[self.ql])
        except:
            if self.ql in models:
                urllib.request.urlretrieve(
                    "https://github.com/maria-terekhina/search_kwic/raw/master/udpipe-ud-2.0-170801/{}".format(models[self.ql]),
                    models[self.ql])
                self.model_ql = Model(models[self.ql])
            else:
                raise ValueError('No model for this language.')

        try:
            self.model_tl = Model(models[self.tl])
        except:
            if self.tl in models:
                urllib.request.urlretrieve(
                    "https://github.com/maria-terekhina/search_kwic/raw/master/udpipe-ud-2.0-170801/{}".format(models[self.tl]),
                    models[self.tl])
                self.model_tl = Model(models[self.tl])
            else:
                raise ValueError('No model for this language.')

    def align(self, query, sent_q, sent_t):
        '''
        Find translation of the query in target-language sentence.
        :param query: str, query word
        :param sent_q: str, sentence in the original language
        :param sent_t: str, sentence in the target language
        :return: list, indexes of the found word
        '''

        # substitute «» quotes with double quotes («» are not processed correctly)
        sent_q = re.sub('«|»', '"', sent_q)
        sent_t = re.sub('«|»', '"', sent_t)

        # collect metadata of original and parallel sentences
        info_q = self._process(self.model_ql.tokenize(sent_q), self.model_ql)
        info_t = self._process(self.model_tl.tokenize(sent_t), self.model_tl)

        # find query metadata and words of parallel sentences with high similarity to query metadata
        max_i, max_word, query_info = self._find_parallel(query, info_q, info_t)

        # check if it is one word with highest score, if not chose one of them
        if len(max_i) == 1:
            return [0, 0]
        elif max_i[-1] != max_i[-2]:
            target = max_word[-1]['word']
        else:
            target = self._decision_maker(max_i, max_word, query_info)['word']

        idx = sent_t.find(target)
        return [idx, idx + len(max_word[-1]['word'])]

    def _process(self, sentences, model):
        '''
        Collect metadata of the words.
        :param sentences: list, sentences to collect metadata
        :param model: Model, udpipe mpdel of the sentence language
        :return: list of dicts, metadata of all words in the sentence
        '''

        for s in sentences:
            model.tag(s)
            model.parse(s)
        return self._collect_info(model.write(sentences, "conllu"))

    def _collect_info(self, meta):
        '''
        Collect metadata of all words in the sentence (POStag, parent, children, dependency tag, position in the
        sentence.
        :param meta: str, metadata in CONLLU format
        :return: dict, metadata of all words in the sentence
        '''

        words = {}
        n = 0
        k = 0

        # collect token metadata: word, POS-tag, parent position, syntactic tag, and position in the sentence
        for word in meta.split('\n')[4:]:
            data = word.split('\t')
            if len(data) == 1:
                continue
            else:
                if '-' in data[0]:
                    continue
                else:
                    if int(data[0]) == 1:
                        k = n
                    n += 1
                    words[n] = {'word': data[1],
                                'POS': data[3],
                                'parent': int(data[6]) + k,
                                'tag': data[7],
                                'children': list(),
                                'position': n}

        # collect token metadata: parent tag and children tags
        for i in words:
            if words[i]['tag'] == 'root':
                words[i]['parent_tag'] = None
            else:
                words[i]['parent_tag'] = words[words[i]['parent']]['tag']
                words[words[i]['parent']]['children'].append(words[i]['tag'])
        return words

    def _find_parallel(self, query, info_q, info_t):
        '''
        Compare query metadata with all words in translation sentence.
        :param query: str, query
        :param info_q: dict, metadata of all words in original sentence
        :param info_t: dict, metadata of all words in translation
        :return:
            max_i: list, scores of the words in translation (score is added only if >= previous score in list)
            max_word: list, words, which scores are in max_i
            query_info: dict, query metadata
        '''

        query_info = dict()
        max_i = [0]
        max_word = list()

        # find query info in *info_q*
        for word in info_q:
            if info_q[word]['word'] == query:
                query_info = info_q[word]
                break

        # compare metadata of words in *info_t* with query metadata
        for word in info_t:
            i = 0
            if info_t[word]['POS'] == query_info['POS']:
                i += 1
            if info_t[word]['tag'] == query_info['tag']:
                i += 1
            if info_t[word]['parent_tag'] == query_info['parent_tag']:
                i += 1
            i += len(set(query_info['children'])) - \
                 len(set(query_info['children']) - set(info_t[word]['children']))

            info_t[word]['counter'] = i

            if i >= max_i[-1]:
                max_i.append(i)
                max_word.append(info_t[word])

        return max_i, max_word, query_info

    def _decision_maker(self, max_i, max_word, query_info):
        '''
        Choose the translation word over several candidates based on position relative to query word.
        :param max_i: list, scores of the words in translation (score is added only if >= previous score in list)
        :param max_word: list, words, which scores are in max_i
        :param query_info: dict, query metadata
        :return: str, chosen word
        '''

        n = max_i.count(max_i[-1])
        dist = list()
        # take last words with the same score and find the nearest to query
        for i in max_word[-n:]:
            dist.append(fabs(query_info['position'] - i['position']))

        return max_word[-n:][dist.index(min(dist))]


if __name__ == '__main__':
    a = Aligner('rus', 'eng')
    print(a.align('очки', "Как я уже сказал, наши скамьи были рядом, одна за другой.", " "))