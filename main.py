import sys
import mongo_corpora

from nltk_extractor import TagExtractor

# The tag extraction process is data-driven.  Here is the data that drives it.  
# It specifies which database(s), collections, and fields to operate upon.
databases = {
  'threads': {
    'update posts collection' : { 
      'collection': 'posts',
      'text_field': 'responseDescription',
      'tags_field': 'concepts'
    },

    'update discussions collection': {
      'collection': 'discussions',
      'text_field': 'discussionPrompt',
      'tags_field': 'concepts'
    },

    'update resources collection': {
      'collection': 'resources',
      'text_field': 'text',
      'tags_field': 'concepts'
    },

    'update citations collection': {
      'collection': 'citations',
      'text_field': 'longText',
      'tags_field': 'concepts'
    }
  }
}

PRIORITY = { 
  "VB": 2,
  "NP": 3
}

def get_priority(pos):
  if PRIORITY.get(pos):
    return PRIORITY[pos]
  else:
    sys.stderr.write('No Priority for POS: {0}\n'.format(pos))
    return 0

def tags_to_hash(tags):
  """Convert tags to a form that can be stored in MongoDB""" 
  [{ 
    'tag':      tag.text,             # The tag text (e.g. "bowling ball", "cat", etc.)
    'count':    tag.occurs,           # The number of times that the tag occurs.
    'pos':      tag.pos,              # The part of speech that the tag represents.
    'priority': get_priority(tag.pos) # A numeric representation of the Part of Speech.  
  } for tag in tags]

def main():
  # Create the TagExtractor, a wrapper around the NLTK toolkit.
  extractor = TagExtractor()

  for database_name in databases:
    print 'Database: {0}'.format(database_name)
    for job_name in databases[database_name]:
      job = databases[database_name][job_name]

      collection = job['collection']
      text_field = job['text_field']
      tags_field = job['tags_field']

      print
      print '   In collection: {0}, extracting tags from field: {1} and storing them in field: {2}'.format(collection, text_field, tags_field)

      corpora = mongo_corpora.get_corpora(database = database_name, collection = collection)

      for corpus in corpora.get_all():
        text = corpus.get_text(text_field) 
        if text:
          tags = extractor.extract_tags(text)
          for tag in tags:
            print str(tag)
          corpus.put_tags(tags_field, tags_to_hash(tags))
          corpus.save()

main()
