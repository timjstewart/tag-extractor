import sys

class Corpora:
  
  def get_all(self):
    pass

class Corpus:

  def get_text(self):
    pass

  def put_tags(self, tags):
    pass

PRIORITY = { 
  "VB": 2,
  "NP": 3
}

class Tag:

  def __init__(self, text, occurs, pos):
    self.text = text
    self.occurs = occurs
    self.set_pos(pos)

  def set_pos(self, pos):
    self.pos = pos
    self.priority = self.__get_priority(pos)

  def increment_occurs(self):
    self.occurs = self.occurs + 1
    
  def __str__(self):
    return "Tag: {0} (occurs: {1}, priority: {2}, pos: {3})".format(self.text, self.occurs, self.priority, self.pos)

  def __get_priority(self, pos):
    if PRIORITY.get(pos):
      return PRIORITY[pos]
    else:
      sys.stderr.write('No Priority for POS: {0}\n'.format(pos))
      return 0
    

