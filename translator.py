from requests import post
from bs4 import BeautifulSoup

class Translator:
    def __init__(self, lang):
        self.key = 'dict.1.1.20180108T142346Z.7c55bb77b9772f4d.a3511e096a8db5017f8f3685019e2d823ba15885'
        self.lang = lang
        self.page = None
        self.translations = None

    def get_page(self, text):
        params = {'key': self.key,
                  'lang': self.lang,
                  'text': text}

        s = post('https://dictionary.yandex.net/api/v1/dicservice/lookup', params=params)
        return s

    def get_translations(self):
        translations = []
        soup = BeautifulSoup(self.page.text, 'lxml')

        for transl in soup.select('tr > text'):
            translations.append(transl.text)
        return translations

    def translate(self, text):
        self.page = self.get_page(text)
        return self.get_translations()