import string
import sys
import re
import nltk

from tag import Tag
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.tokenize.regexp import WhitespaceTokenizer

WORD_RE = re.compile('[^a-zA-Z]*([a-zA-Z-\'\.]*[a-zA-Z])[^a-zA-Z]*')
STOP_WORDS = stopwords.words('english')
STOP_WORDS.extend(["i'm"])

GRAMMAR = """
  NP:  {<JJ.*>*<NN.*>+}
  VB:  {<VB.*>+}
  ADV: {<RB.*>+}
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

def tag_compare_key(tag):
  return tag.text

class TagExtractor:
  """Extracts tags from a body of text using the NLTK toolkit."""
  
  def __init__(self):
    """Creates a default Topia tagger and extractor."""
    self.sentence_tokenizer = PunktSentenceTokenizer()
    self.parser = nltk.RegexpParser(GRAMMAR)
    self.productions = ['NP', 'VB', 'ADV']

  def __is_just_stop_words(self, words):
    return not any([word not in STOP_WORDS for word in words])

  def extract_tags(self, text):
    """Extract tags from the text."""
    tags = {} 
    for sentence in self.sentence_tokenizer.tokenize(text):
      chunks = self.__chunk_sentence(sentence)
      for production in chunks.productions():
        tag_tokens = []
        pos = production.lhs().symbol()
        if pos in self.productions:
          for (word, x) in production.rhs():
            # Preprocess, and potentially, filter out the word.
            trimmed = filter_word(trim_word(word))
            if trimmed:
              tag_tokens.append(trimmed.lower())
          if len(tag_tokens) > 0:
            tag_text = string.join(tag_tokens, ' ')
            if self.__is_just_stop_words(tag_tokens):
              continue
            tag = self.__lookup_tag(tags, tag_text, pos) 
            tag.increment_occurs()
            tag.set_pos(pos)
    results = tags.values()
    results.sort(key = tag_compare_key)
    return results

  def __lookup_tag(self, tags, text, pos):
    tag = tags.get(self.__get_tag_key(text, pos))
    if not tag:
      tag = Tag(text, 0, pos)
      tags[self.__get_tag_key(text, pos)] = tag
    return tag

  def __get_tag_key(self, text, pos):
    """I want to keep the way we look up tags flexible so that I can easily change my mind
       on what uniquely identifies a tag (e.g. just the text?  the text and the part of speech?).
       That is why all the logic for looking up tags is in this one method."""
    return text
    
  def __chunk_sentence(self, sentence):
    """Tokenize the sentence into words using a whitespace parser to avoid parsing couldn't into two tokens (could and n't).
       Then chunk the tokens according to GRAMMAR.
    """
    tokenizer = WhitespaceTokenizer()
    tokens = tokenizer.tokenize(sentence)
    pos_tagged = nltk.pos_tag(tokens)
    return self.parser.parse(pos_tagged)

