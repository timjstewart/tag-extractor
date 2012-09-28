##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Term Extractor
$Id: extract.py 100557 2009-05-30 15:48:36Z srichter $
"""
import sys
import string
import zope.interface

from myopia.termextract import interfaces, tag

SEARCH = 0
NOUN = 1

def permissiveFilter(word, part_of_speech, occur, strength):
    return True

class DefaultFilter(object):

    def __init__(self, singleStrengthMinOccur = 3, noLimitStrength = 2, ignored_pos = None):
        self.singleStrengthMinOccur = singleStrengthMinOccur
        self.noLimitStrength = noLimitStrength
        self.ignored_pos = ignored_pos

    def __contains_letters(self, str):
      return 1 in [c in str for c in string.ascii_letters]

    def __call__(self, word, pos, occur, strength):
        if not self.__contains_letters(word):
          return False
        if self.ignored_pos and pos in self.ignored_pos:
          return False
        if len(word) < 2:
          return False
        try:
          sys.stdout.write("Accepted: '" + word + "' ")
        except:
          print("Unable to print word")
        print "(" + pos + ")"
        return ((strength == 1 and occur >= self.singleStrengthMinOccur) or
                (strength >= self.noLimitStrength))

def _add(term, norm, multiterm, terms, tag, pos):
    multiterm.append((term, norm))
    terms.setdefault(norm, 0)
    terms[norm] += 1
    pos[norm] = tag

class TermExtractor(object):
    zope.interface.implements(interfaces.ITermExtractor)

    def __init__(self, tagger=None, filter=None):
        if tagger is None:
            tagger = tag.Tagger()
            tagger.initialize()
        self.tagger = tagger
        if filter is None:
            filter = DefaultFilter()
        self.filter = filter

    def extract(self, taggedTerms):
        """See interfaces.ITermExtractor"""
        terms = {}
        pos = {}
        # Phase 1: A little state machine is used to build simple and
        # composite terms.
        multiterm = []
        state = SEARCH
        while taggedTerms:
            term, tag, norm = taggedTerms.pop(0)
            term = term.lower()
            norm = norm.lower()
            if state == SEARCH and tag.startswith('N'):
                state = NOUN
                _add(term, norm, multiterm, terms, tag, pos)
            elif state == SEARCH and tag == 'JJ' and term[0].isupper():
                state = NOUN
                _add(term, norm, multiterm, terms, tag, pos)
            elif state == NOUN and tag.startswith('N'):
                _add(term, norm, multiterm, terms, tag, pos)
            elif state == NOUN and not tag.startswith('N'):
                state = SEARCH
                if len(multiterm) > 1:
                    word = ' '.join([word for word, norm in multiterm])
                    terms.setdefault(word, 0)
                    terms[word] += 1
                    pos[word] = tag
                multiterm = []
        # Phase 2: Only select the terms that fulfill the filter criteria.
        # Also create the term strength.
        return [
            (word, occur, len(word.split()))
            for word, occur in terms.items()
            if self.filter(word, pos[word], occur, len(word.split()))]

    def __call__(self, text):
        """See interfaces.ITermExtractor"""
        terms = self.tagger(text)
        return self.extract(terms)

    def __repr__(self):
        return '<%s using %r>' %(self.__class__.__name__, self.tagger)
