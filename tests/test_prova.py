import pytest
from concord import Morphit


def empty_test():
    w = Morphit('spaghetti')
    assert w.lemma == "cane"