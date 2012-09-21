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

