 #  File: search.py
 #  Project: Forking Stories
 #  Component: Search engine
 #
 #  Authors:    Dominic May;
 #              Lord_DeathMatch;
 #              Mause
 #
 #  Description: uses the tf-idf algorithm to search the stories
from __future__ import print_function


# stlid imports
import re
import os
import math
import json
import time
import logging
from itertools import chain
from collections import defaultdict, Counter

# un-comment this line for debugging stuff
#logging.debug = print
#logging.debug = logging.info

# project imports
from dbapi.story import Story
from dbapi import searchindex

############ Index computation code ############


class Document(object):
    with open(os.path.join('resources', 'stopwords.json')) as fh:
        stopwords = set(json.load(fh))
    TOKEN_RE = re.compile(r"\w+", flags=re.UNICODE)

    def __init__(self, raw, name=None):
        self.name = name

        self.tokens, self.num_tokens = tokenize(raw, self.TOKEN_RE)
        self.tokens = list(filter(lambda x: x not in self.stopwords, self.tokens))

        self.freq_map = Counter(self.tokens)

        self.tokens = set(self.tokens)


def tokenize(x, TOKEN_RE):
    x = x.lower()
    x = TOKEN_RE.findall(x)
    return x, len(x)


def term_freq(word, document, all_documents):
    maximum_occurances = max(document.freq_map.values())
    if not maximum_occurances:
        return document.freq_map[word]
    return document.freq_map[word] / float(maximum_occurances)


def inverse_document_freq(word, document, all_documents):
    instances_in_all = len([1 for document in all_documents if word in document.tokens])
    if not instances_in_all:
        return 1
    return math.log(len(all_documents) / instances_in_all)


def build_index(directory):

    # read in the documents
    start = time.time()
    logging.debug('Reading in and tokenising the documents started at {}'.format(start))

    # grab the stories (headers for the stories anyway)
    stories = Story.find('all', '')

    # load in the documents
    all_documents = []
    for story in stories:
        logging.debug('\t *', story.title)
        content = story.title + ' ' + ' '.join([paragraph.content for paragraph in story.get_approved_paragraphs()])
        all_documents.append(Document(content, name=story.id))

    logging.debug('Ended after {} seconds'.format(time.time() - start))

    start = time.time()
    logging.debug('Computing the word relevancy values started at {}'.format(start))

    # compute the index
    index = defaultdict(defaultdict)
    for document in all_documents:
        for word in document.tokens:
            index[document.name][word] = (
                term_freq(word, document, all_documents) *
                inverse_document_freq(word, document, all_documents)
            )

    logging.debug('Ended after {} seconds'.format(time.time() - start))
    return index

############ Index storage code ############


def load_index(cursor, conn):
    # read in the index, if it is cached
    index_models = searchindex.SearchIndex.all(cursor)
    index = defaultdict(defaultdict)

    # reformat index models into usuable format
    for model in index_models:
        index[model.identifier] = model.index

    # save the index
    if not index:
        index = build_index(os.getcwd())
        logging.debug('Index built. Saving to db')
        start = time.time()
        save_index(cursor, conn, index)
        logging.debug('Saved to db. Took {} seconds'.format(time.time() - start))

    # pprint(index)
    return index


def save_index(cursor, conn, index):
    for document in index.keys():
        document_index = searchindex.SearchIndex(
            identifier=document, index=index[document])
        document_index.put(cursor, conn)


def search(cursor, conn, query):

    index = load_index(cursor, conn)

    logging.debug('Docs; {}'.format(len(index)))
    words = [x.lower() for x in query.split()]

    logging.debug('End query; {}'.format(words))
    # logging.debug('Unique indexed words;', len(list(set(chain.from_iterable([x.keys() for x in index.values()])))))
    logging.debug('Unique indexed words; {}'.format(len(list(set(chain.from_iterable([x.keys() for x in index.values()]))))))
    scores = defaultdict(float)
    for page in index:
        for word in words:
            if word in index[page]:
                scores[page] += index[page][word]

    logging.debug('Relevant pages; {}'.format(len(scores)))
    scores = sorted(scores.items(), key=lambda x: x[1])[::-1]

    return scores


def main():
    # make sure we are using the same database as the rest of the code
    from dbapi import conn
    cursor = conn.cursor()

    searchindex.create_table(conn, True)

    # do the search function
    results = search(cursor, conn, input('Q? '))
    print()
    for result in results:
        print(Story.find('id', result[0])[0].title, '-->', result[1])

    conn.close()


if __name__ == '__main__':
    main()
