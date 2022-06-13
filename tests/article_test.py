import pytest
from pymorphit import Morphit


def empty_test():
    w = Morphit('spaghetti')
    assert w.lemma == "cane"

    
def test_orso():
    
    a = Morphit("orso")
    b = Morphit("orsi")

    assert a.is_spurious() == False
    assert a.is_vocalic() == True
    assert a.article() == "l'"
    assert a.article(form="i") == "un"

    assert b.is_spurious() == False
    assert b.is_vocalic() == True
    assert b.article() == "gli"
    

def test_orso():
    
    a = Morphit("gnomo")
    b = Morphit("gnomi")
    
    assert a.article() == "lo"
    assert a.article(form="i") == "uno"
    assert b.article() == "gli"


def test_aquila():    
    
    a = Morphit("aquila")
    b = Morphit("aquile")
    
    assert a.article() == "l'"
    assert a.article(form="i") == "un'"
    assert b.article() == "le"


def test_gatta():    
    
    a = Morphit("gatta")
    b = Morphit("gatte")
    
    assert a.article() == "la"
    assert a.article(form="i") == "una"
    assert b.article() == "le"
    
    
def test_maiale():    
    
    a = Morphit("maiale")
    b = Morphit("maiali")
    
    assert a.article() == "il"
    assert a.article(form="i") == "un"
    assert b.article() == "i"