from tagging import Tag

from myopia.termextract import extract, tag

class TagExtractor:
  """Extracts tags from a body of text"""
  
  def __init__(self):
    """Creates a default Topia tagger and extractor"""
    self.__init_tagger()
    self.__init_extractor()

  def tune_filter(self, min_unigram_freq, min_n):
    """Tune the filter"""
    self.extractor.filter = extract.DefaultFilter(min_unigram_freq, min_n, ["RB", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])

  def extract_tags(self, text):
    """Extract tags from the text"""
    return [Tag(t,o,s) for (t,o,s) in self.extractor(text)]

  def __init_tagger(self):
    self.tagger = tag.Tagger()
    self.tagger.initialize()

  def __init_extractor(self):
    self.extractor = extract.TermExtractor(self.tagger)
    self.extractor.filter = extract.permissiveFilter

