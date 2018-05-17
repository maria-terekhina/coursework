search_kwic
==========


# Documentation

`search_kwic` is a simple tool for presentation of parallel text in the KWIC format. First of all, see Installation and then proceed to Qwick start.

## Installation 

To install serach_kwic type in the terminal:

    pip install search_kwic 

search_kwic depends on `ufal.udpipe`, it will be install during the `search_kwic` installation.

## Quickstart

To find a token in parallel text, which corresponds to the query in the original text use an instance of `Aligner` object and method `align`. It will return indexes of corresponding word in parallel text.


```python
from search import Aligner
```


```python
aligner = Aligner(queryLanguage='rus', targetLanguage='eng')
```


```python
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



## How to use

`Aligner` takes to positional arguments:
- **`queryLanguage`**: language of original sentence(s)
- **`targetLanguage`**: language of parallel sentence(s), where you want to find a corresponding word

`Aligner` has one method `align`, which takes three positional arguments:
- **`query`**: word to which you want to find a corresponding one in parallel text
- **`sent_q`**: original sentence(s) containing query
- **`sent_t`**: parallel sentence(s)


```python

```
