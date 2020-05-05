```python
from concord import Morphit

w = Morphit('spaghetti')
```


```python
w.lemma
```




    'spaghetto'




```python
w.pos
```




    'NOUN'




```python
w.gender
```




    'm'




```python
w.number
```




    'p'




```python
w.features
```




    {'gender': 'm', 'number': 'p', 'pos': 'NOUN', 'lemma': 'spaghetto'}




```python
w.article()
```




    'gli'




```python
w.get_singular()
```




    'spaghetto'




```python
w.preposition('di')
```




    'degli'




```python
w.concord('volava')
```




    'volavano'




```python
w.concord('volerà')
```




    'voleranno'




```python
w.concord('volato')
```




    'volati'




```python
w.concord('volare')
```




    'volano'


