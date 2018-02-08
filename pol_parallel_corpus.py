from params_container import Container
from requests import post
from bs4 import BeautifulSoup
import pandas
import re
from kwic_for_corpora import DictionaryKwic

class PageParser:
    def __init__(self, query, numResults, language, targetLanguage):
        self.query = query
        self.page = None
        self.numResults = numResults
        self.language = language
        self.targetLanguage = targetLanguage

    def get_page(self):

        lang = re.sub(self.language, self.language[0].upper()+self.language[1:], self.language)

        params = {'string' + self.language: self.query,
                  'limit' + lang: self.numResults,
                  '1': 'on',
                  '2': 'on',
                  '3': 'on',
                  '4': 'on',
                  '5': 'on',
                  'polish': 'on',
                  'russian': 'on',
                  'foreign': 'on'}
        s = post('http://pol-ros.polon.uw.edu.pl/searchresults/searchwru.php', params=params)
        return s

    def get_results(self):
        original = []
        translation = []
        soup = BeautifulSoup(self.page.text, 'lxml')
        for orig in soup.select('.resultsleftcol'):
            original.append(orig.text)
        for tran in soup.select('.resultsrightcol'):
            translation.append(tran.text)

        s = [[original[i].lower(), translation[i].lower()] for i in range(len(original))]
        return s

    def extract_results(self):
        self.page = self.get_page()
        parsed_results = self.get_results()
        return parsed_results


class Downloader(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def download_all(self):
        parser = PageParser(self.query, self.numResults, self.language, self.targetLanguage)
        try:
            return parser.extract_results()
        except:
            return []


def main(query='удар', language='ru', targetLanguage='pl', numResults=100, write=False):
    downloader = Downloader(query, language, targetLanguage, numResults, write)
    results = downloader.download_all()
    print(pandas.DataFrame(results))

    dkwic = DictionaryKwic(query, language, targetLanguage)
    kwic_res, other = dkwic.results_to_kwic(results)
    print(len(kwic_res)/(len(other)+len(kwic_res)))


    return results


if __name__ == '__main__':
    #unittest.main()
    '''args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    #parser.add_argument('corpus', type=str)
    parser.add_argument('query', type=str)
    parser.add_argument('numResults', type=int)
    parser.add_argument('write', type=bool)
    parser.add_argument('language', type=str)
    parser.add_argument('targetLanguage', type=str)
    args = parser.parse_args(args)
    main(**vars(args))'''
    main()
