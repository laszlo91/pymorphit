# Concord #

A sample toolkit for Italian NLP, powered by Morphit.


```python
from concord import Morphit

w = Morphit('spaghetti')

# Attributes:

w.lemma
#'spaghetto'

w.pos
#'NOUN'

w.gender
#'m'

w.number
#'p'

w.features
#{'gender': 'm', 'number': 'p', 'pos': 'NOUN', 'lemma': 'spaghetto'}
```

The following methods get the corrisponding form, if existing in Morphit.


```python
w.get_singular()
#'spaghetto'

w.get_female()
# None

w.get_plural()
#'spaghetti'

w.get_male()
#'spaghetti'

w0 = Morphit('vedevi')
w0.get_plural()
#'vedevate'
```

A method .article() ('definite' by default) returns the right article form, while a method .preposition(p) allows to build compound prepositions (preposition + definite article). Composable prepositions are 'di', 'a', 'da', 'in', 'su'.


```python
w.article()
#'gli'

w.preposition('di')
#'degli'

w0 = Morphit('spaghetto')
w0.article('indefinite')
#'uno'
```

.agr(word): agr stands for agreement. It returns the correct inflection of the argument, based on the Morphit object, which works as the head. You can use it to get the agreement between a noun (or a personal pronoun) and an adjective (or other types of attributes and determiners) or a verb.


```python
w.agr('volava')
#'volavano'

w.agr('volato')
#'volati'

w.agr('volare')
#'volano'

w.agr('deliziose')
#'deliziosi'

w0 = Morphit('noi', 'PRO-PERS', 'f')
w0.agr('mangerei')
#'mangeremmo'
```

Both to Morphit() or self.agr() you might have to add optional arguments to avoid ambiguities between forms. 

## Credits ##

* [morph-it](http://sslmitdev-online.sslmit.unibo.it/linguistics/morph-it.php) lexical data by [Scuola di Lingue e Letterature, Traduzione e Interpretazione, Università di Bologna]( http://www.scuolalingue.unibo.it/it)
