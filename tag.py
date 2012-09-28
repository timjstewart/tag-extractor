import sys


class Tag:

  def __init__(self, text, occurs, pos):
    self.text = text
    self.occurs = occurs
    self.set_pos(pos)

  def set_pos(self, pos):
    self.pos = pos

  def increment_occurs(self):
    self.occurs = self.occurs + 1
    
  def __str__(self):
    return "Tag: {0} (occurs: {1}, pos: {2})".format(self.text, self.occurs, self.pos)

   
