from model import Model
from math import fabs
models = {'rus': 'russian-syntagrus-ud-2.0-170801.udpipe',
          'eng': 'english-ud-2.1-20180111.udpipe',
          'ita': 'italian-ud-2.0-170801.udpipe'}


class Aligner:

    def __init__(self, queryLanguage, targetLanguage):
        self.ql = queryLanguage
        self.tl = targetLanguage

        self.model_ql = Model(models[self.ql])
        self.model_tl = Model(models[self.tl])

    def find_parallel_(self, query, info_q, info_t):
        '''
        Compare query metadata with all words in translation sentence.
        :param query: str, query
        :param info_q: list of dicts, metadata of all words in original sentence
        :param info_t: list of dicts, metadata of all words in translation
        :return:
            max_i: list, scores of the words in translation (score is added only if >= previous score in list)
            max_word: list, words, which scores are in max_i
            query_info: dict, query metadata
        '''

        query_info = dict()
        max_i = [0]
        max_word = list()

        for sent in info_q:
            for word in sent:
                if sent[word]['word'] == query:
                    query_info = sent[word]
                    break

        for sent in info_t:
            for word in sent:
                i = 0
                if sent[word]['POS'] == query_info['POS']:
                    i += 1
                if sent[word]['tag'] == query_info['tag']:
                    i += 1
                if sent[word]['parent_tag'] == query_info['parent_tag']:
                    i += 1
                i += len(set(query_info['children'])) - \
                     len(set(query_info['children']) - set(sent[word]['children']))

                sent[word]['counter'] = i

                if i >= max_i[-1]:
                    max_i.append(i)
                    max_word.append(sent[word])

        return max_i, max_word, query_info

    def decision_maker_(self, max_i, max_word, query_info):
        '''
        Choose the translation word over several candidates.
        :param max_i: list, scores of the words in translation (score is added only if >= previous score in list)
        :param max_word: list, words, which scores are in max_i
        :param query_info: dict, query metadata
        :return: str, chosen word
        '''

        n = max_i.count(max_i[-1])
        dist = list()

        for i in max_word[-n:]:
            dist.append(fabs(query_info['position'] - max_word[i]['position']))

        return max_word[-n:][dist.index(min(dist))]

    def align(self, query, sent_q, sent_t):
        '''
        Find translation of the query in target-language sentence.
        :param query: str, query word
        :param sent_q: str, sentence in the original language
        :param sent_t: str, sentence in the target language
        :return: list, indexes of the found word
        '''

        info_q = [sent for sent in self.process_(self.model_ql.tokenize(sent_q), self.model_ql)]
        info_t = [sent for sent in self.process_(self.model_tl.tokenize(sent_t), self.model_tl)]

        max_i, max_word, query_info = self.find_parallel_(query, info_q, info_t)
        print(max_word[-1]['word'])

        if max_i[-1] == max_i[-2]:
            target = self.decision_maker_(max_i, max_word, query_info)['word']
        else:
            target = max_word[-1]['word']

        idx = sent_t.find(target)
        return [idx, idx+len(max_word[-1]['word'])]

    def process_(self, sentences, model):
        '''
        Collect metadata of the words.
        :param sentences: list, sentences to collect metadata
        :param model: Model, udpipe mpdel of the sentence language
        :return: list of dicts, metadata of all words in the sentence
        '''

        for s in sentences:
            model.tag(s)
            model.parse(s)
        yield self.collect_info_(model.write(sentences, "conllu"))

    def collect_info_(self, meta):
        '''
        Collect metadata of all words in the sentence (POStag, parent, children, dependency tag, position in the
        sentence.
        :param meta: str, metadata in CONLLU format
        :return: dict, metadata of all words in the sentence
        '''
        words = {}
        n = 0
        k = 0
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
        for i in words:
            if words[i]['tag'] == 'root':
                words[i]['parent_tag'] = None
            else:
                words[i]['parent_tag'] = words[words[i]['parent']]['tag']
                words[words[i]['parent']]['children'].append(words[i]['tag'])

        return words



if __name__ == '__main__':
    a = Aligner('rus', 'ita')
    a.align('стол', 'Сразу за дверью помещался длинный письменный стол. Здесь трудилась Ракель, выполняя обязанности одновременно распорядителя и секретаря.',
            "Immediatamente di fronte all'ingresso c'era la lunga scrivania di legno dove Raquel svolgeva allo stesso tempo la funzione di receptionist e di segretaria.")