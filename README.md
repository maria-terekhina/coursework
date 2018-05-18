search_kwic
==========


# Documentation

`search_kwic` is a simple tool for presentation of parallel text in the KWIC format. First of all, see Installation and then proceed to Qwick start.

## Installation 

To install `serach_kwic` type in the terminal:

    pip install search_kwic 

`search_kwic` depends only on `ufal.udpipe`, it will be installed during the `search_kwic` installation.

## Quickstart

To find a token in parallel text, which corresponds to the query in the original text use an instance of `Aligner` object and method `align`. It will return indexes of corresponding word in parallel text.


```python
from search import Aligner

aligner = Aligner(queryLanguage='rus', targetLanguage='eng')
idxs = aligner.align(query='очки', sent_q='На шее висели очки на цепочке в роговой оправе и с толстыми стеклами.',
                            sent_t='The horn-rimmed glasses hanging around her neck were thick.')
idxs
```




    [16, 23]




```python
phrase = 'The horn-rimmed glasses hanging around her neck were thick.'
phrase[idxs[0]:idxs[1]]
```




    'glasses'



## Descriprion

`search_kwic` uses [Universal Dependencies models](http://universaldependencies.org/) provided by [Udpipe](http://ufal.mff.cuni.cz/udpipe) to find a corresponding word in parallel sentence.

#### Arguments

`Aligner` takes to positional arguments:
- **`queryLanguage`**: language of original sentence(s)
- **`targetLanguage`**: language of parallel sentence(s), where you want to find a corresponding word

`Aligner` has one method `align`, which takes three positional arguments:
- **`query`**: word to which you want to find a corresponding one in parallel text
- **`sent_q`**: original sentence(s) containing query
- **`sent_t`**: parallel sentence(s)

#### Output

`align` returns **list** of indexes of the corresponding word found in the parallel text.

## Avaliable languages

List of avaliable languages is limited only by avaliable pretrained UD models. The list of currently avaliable languages is the following (codes are in the [ISO_639-1 format](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)):

| Code  | Language |
| ------------- | ------------- |
|ara|arabic|
|eus|basque|
|bel|belarusian|
|bul|bulgarian|
|cat|catalan|
|zho|chinese|
|cop|coptic|
|hrv|croatian|
|ces|czech|
|dan|danish|
|nld|dutch|
| eng | english  |
|est|estonian|
|fin|finnish|
|fra|french|
|glg|galician|
|got|gothic|
|ell|greek|
|heb|hebrew|
|hin|hindi|
|hun|hungarian|
|ind|indonesian|
|gle|irish|
| ita | italian  |
|jpn|japanese|
|kaz|kazakh|
|kor|korean|
|lat|latin|
|lit|lithuanian|
|nor|norwegian|
|chu|old_church_slavonic|
|fas|persian|
|pol|polish|
|por|portugese|
|ron|romanian|
|rus|russian|
|san|sanskrit|
|slk|slovak|
|slv|slovenian|
|spa|spanish|
|swe|swedish|
|tam|tamil|
|tur|turkish|
|ukr|ukranian|
|urd|urdu|
|uig|uyghur|
|vie|vietnamese|

## License

The package is destriduted under the MIT license, read about it [here](https://github.com/maria-terekhina/search_kwic/blob/master/LICENSE).
