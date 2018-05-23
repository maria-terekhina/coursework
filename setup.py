from setuptools import setup

setup(
  name = 'search_kwic',
  packages = ['search_kwic'],
  version = '0.1',
  description = 'Tool for KWIC representation of paralleltext. Find a word in parallel text corresponding to query in original text.',
  author = 'Maria Terekhina',
  author_email = 'maria.myslina@gmail.com',
  url = 'https://github.com/maria-terekhina/search_kwic',
  download_url = 'https://github.com/maria-terekhina/search_kwic/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['kwic', 'parallel', 'corpora', 'alignment'], 
  classifiers = [],
  install_requires=['ufal.udpipe']
)