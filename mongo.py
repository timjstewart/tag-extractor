import pymongo
from tagging import Corpus, Corpora

class DocumentCorpus(Corpus):
  """A corpus of text taken from a document"""

  def __init__(self, collection, document):
    self.collection      = collection
    self.document        = document 

  def get_text(self, text_field):
    """Returns the text from the document"""
    return self.document[text_field]

  def put_tags(self, tags_field, tags):
    """Update the tags in the document"""
    self.document[tags_field] = tags

  def save(self):
    self.collection.save(self.document)

class CollectionCorpora(Corpora):
  """Corpora stored in a MongoDB collection"""

  def __init__(self, server, port, database_name, collection_name):
    self.server     = server
    self.port       = port
    self.connection = pymongo.Connection(server, port)
    self.database   = self.connection[database_name]
    self.collection = self.database[collection_name]

  def get_all(self):
    """Returns all the Corporus objects found in the MongoDB collection"""
    return [DocumentCorpus(self.collection, document) for document in self.collection.find()]

def get_corpora(**args):
  """Returns a Corpora object based on the MongoDB parameters supplied"""

  host = args.pop('host', 'localhost')
  port = args.pop('port', 27017)

  database = args.pop('database')
  if not database:
    raise Exception('database parameter is required')

  collection = args.pop('collection', None)
  if not collection:
    raise Exception('collection parameter is required')

  return CollectionCorpora(host, port, database, collection)
