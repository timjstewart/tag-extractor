from topia.termextract import extract, tag

class Corpora:
  
  def get_all(self):
    pass

class Corpus:

  def get_text(self):
    pass

  def put_tags(self, tags):
    pass

class Tag:

  def __init__(self, text, occurs, strength):
    self.text = text
    self.occurs = occurs
    self.strength = strength

  def __str__(self):
    return "{0} (occurs: {1}, strength: {2})".format(self.text, self.occurs, self.strength)

class TagExtractor:
  """Extracts tags from a body of text"""
  
  def __init__(self):
    """Creates a default Topia tagger and extractor"""
    self.__init_tagger()
    self.__init_extractor()

  def tune_filter(self, min_unigram_freq, min_n):
    """Tune the filter"""
    self.extractor.filter = extract.DefaultFilter(min_unigram_freq, min_n)

  def extract_tags(self, text):
    """Extract tags from the text"""
    return [Tag(t,o,s) for (t,o,s) in self.extractor(text)]

  def __init_tagger(self):
    self.tagger = tag.Tagger()
    self.tagger.initialize()

  def __init_extractor(self):
    self.extractor = extract.TermExtractor(self.tagger)
    self.extractor.filter = extract.permissiveFilter

