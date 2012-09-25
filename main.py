import sys
import mongo

from topia_extractor import TagExtractor

extractor = TagExtractor()
extractor.tune_filter(1, 1)

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

def tags_to_hash(tags):
  result = []
  for tag in tags:
    result.append({ 'tag': tag.text, 'count': tag.occurs })
  return result

for database_name in databases:
  print 'Database: {0}'.format(database_name)
  for job_name in databases[database_name]:
    job = databases[database_name][job_name]

    collection = job['collection']
    text_field = job['text_field']
    tags_field = job['tags_field']

    print
    print '   In collection: {0}, extracting tags from field: {1} and storing them in field: {2}'.format(collection, text_field, tags_field)

    corpora = mongo.get_corpora(database = database_name, collection = collection)

    for corpus in corpora.get_all():
      text = corpus.get_text(text_field) 
      if text:
        tags = extractor.extract_tags(text)
        corpus.put_tags(tags_field, tags_to_hash(tags))
        corpus.save()
        sys.stdout.write('.')

    print

