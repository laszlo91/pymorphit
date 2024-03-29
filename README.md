# pymorphit #

This library uses Morphit (a free morphological resource for Italian) to describe the morphology of a word, and to retrieve its correct inflected form whenever it has a dependency relation with another one. 
It can be used for simple placeholder sentence generation (see the jupyter example for more details)

Under construction. You can test it with pip:

```
pip install git+https://github.com/laszlo91/pymorphit.git

```

Some usage example:


```python
from pymorphit import Morphit

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

The following methods get the corrisponding form, if existing in the Morphit. pymorphit doesn't actually use the original Morphit file, but a pickle compact version containings just the inflected parts of speech. If you want to add some new word to the Morphit pickle, please have a look to the command-line script add2morphit.py


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

There's a method to get the right article form (both definite and indefinite) or to build compound prepositions (preposition + definite article). Composable prepositions are 'di', 'a', 'da', 'in', 'su'.


```python
w.article()
#'gli'

w.preposition('di')
#'degli'

w0 = Morphit('spaghetto')
w0.article('indefinite')
#'uno'
```

AGR stands for agreement. This method returns the correct inflection of the argument, being dependent of Morphit object, which then works as the head. You can use it to get the agreement between a noun (or a personal pronoun) and an adjective (or other types of attributes and determiners) or a verb.


```python
w.word
#'spaghetti'

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

You might have to add optional arguments when you initialize the Morphit object, in order to avoid ambiguities between forms.

Here the allowed arguments:

Parts of speech: **['VER', 'AUX', 'CAU', 'ASP', 'ADJ', 'DET-POSS', 'DET-WH', 'TALE', 'DET-INDEF', 'NOUN', 'PRO-PERS', 'CLI']**

Verbal modes: **['cond', 'ger', 'impr', 'ind', 'inf', 'part', 'sub']**

Person of the verbs: **[1, 2, 3]**

Gender: **['m', 'f']**

Number: **['s', 'p']**

## Bonus ##

http://phillipo.pythonanywhere.com/ <--- A flask web-app to compose anagrams (again, powered by Morphit)

## Credits ##

* [morph-it](http://sslmitdev-online.sslmit.unibo.it/linguistics/morph-it.php) lexical data by [Scuola di Lingue e Letterature, Traduzione e Interpretazione, Università di Bologna]( http://www.scuolalingue.unibo.it/it)
