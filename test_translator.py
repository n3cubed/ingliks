from py.ingliks import Translator

translator = Translator()


def test_something():
  assert (translator.translate('hello') == ('helq', []))
