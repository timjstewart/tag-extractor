import string
import sys
import re
import nltk

from tagging import Tag
from nltk.tokenize.punkt import PunktSentenceTokenizer

WORD_RE = re.compile('[^a-zA-Z]*([a-zA-Z-\.]*[a-zA-Z])[^a-zA-Z]*')

GRAMMAR = """
  NP:  {<JJ.*>*<NN.*>+}
  VB:  {<VB.*>+}
  """

def filter_word(word):
  """Decide if the word should be included in the tag collection."""
  if word and len(word) > 1:
    return word
  else:
    return None

def trim_word(word):
  """Trim extra characters from the word (e.g. trailing parenthesis)"""
  if not word:
    return None
  match = WORD_RE.search(word)
  if match:
    tokens = []
    for token in match.groups():
      tokens.append(token)
    return string.join(tokens, ' ')
  else:
    return None

class TagExtractor:
  """Extracts tags from a body of text using the NLTK toolkit."""
  
  def __init__(self):
    """Creates a default Topia tagger and extractor"""
    self.sentence_tokenizer = PunktSentenceTokenizer()
    self.parser = nltk.RegexpParser(GRAMMAR)
    self.productions = ['NP', 'VB']

  def extract_tags(self, text):
    """Extract tags from the text"""
    tags = {} 
    for sentence in self.sentence_tokenizer.tokenize(text):
      chunks = self.__chunk_sentence(sentence)
      for production in chunks.productions():
        tag_tokens = []
        pos = production.lhs().symbol()
        if pos in self.productions:
          for (word, x) in production.rhs():
            trimmed = filter_word(trim_word(word))
            if trimmed:
              tag_tokens.append(trimmed.lower())
          if len(tag_tokens) > 0:
            tag_text = string.join(tag_tokens, ' ')
            print tag_text, pos
            tag = self.__find_tag(tags, tag_text, pos) 
            tag.increment_occurs()
            tag.set_pos(pos)
    return tags.items()

  def __find_tag(self, tags, text, pos):
    tag = tags.get(text)
    if not tag:
      tag = Tag(text, 1, pos)
    return tag
    
  def __chunk_sentence(self, sentence):
    tokens = nltk.word_tokenize(sentence)
    pos_tagged = nltk.pos_tag(tokens)
    return self.parser.parse(pos_tagged)

