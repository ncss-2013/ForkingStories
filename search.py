 #  File: search.py
 #
 #  Project: Forking Stories
 #  Component: Search engine
 #
 #  Authors:    Dominic May;
 #              Lord_DeathMatch;
 #              Mause
 #
 #  Description: uses the tf-idf algorithm to search the stories


# stlid imports
import re
import os
import math
import json
import time
import pickle
import sqlite3
import logging
from itertools import chain
from collections import defaultdict, Counter

# un-comment this line for debugging stuff
# logging.debug = print

# project imports
from dbapi.story import Story

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
        return 0
    return math.log(len(all_documents) / instances_in_all)


def build_index_for_doc(document, all_documents):
    for word in document.tokens:
        yield (
            word,
            (
                term_freq(word, document, all_documents) *
                inverse_document_freq(word, document, all_documents)
            ))


def build_index(directory):

    # read in the documents
    start = time.time()
    logging.debug('Reading in and tokenising the documents started at {}'.format(start))

    all_documents = []
    stories = Story.find('all', '')

    for story in stories:
        logging.debug('\t *', story.title)
        content = ''.join([
            para.content + ' '
            for para in story.get_approved_paragraphs()])
        all_documents.append(Document(content, name=story.id))

    logging.debug('Ended after {}'.format(time.time() - start))

    start = time.time()
    logging.debug('Computing the word relevancy values started at {}'.format(start))
    # compute the index
    index = defaultdict(defaultdict)
    for document in all_documents:
        index[document.name] = dict(build_index_for_doc(document, all_documents))
    logging.debug('Ended after {}'.format(time.time() - start))
    return index

############ Index storage code ############


def load_index(cursor, conn):
    # read in the index, if it is cached
    index_models = SearchIndex.all(cursor)
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

    return index


def save_index(cursor, conn, index):
    for document in index.keys():
        document_index = SearchIndex(
            identifier=document, index=index[document])
        document_index.put(cursor, conn)


class SearchIndex(object):
    def __init__(self, identifier, index=None):
        self.identifier = identifier
        self.un_pickled_index = index if type(index) == dict else None
        self.pickled_index = pickle.dumps(index) if type(index) == dict else index

    @property
    def index(self):
        if not self.un_pickled_index:
            return pickle.loads(self.pickled_index)
        else:
            return self.un_pickled_index

    @index.setter
    def index_setter(self, index):
        if type(index) == dict:
            self.un_pickled_index = index
        else:
            self.un_pickled_index = pickle.loads(index)
            self.pickled_index = index

    @classmethod
    def create(*args):
        return SearchIndex(*args)

    @classmethod
    def all(self, cursor):
        query = 'SELECT * FROM SearchIndex'
        cursor.execute(query)
        index_models = [SearchIndex(*q) for q in cursor.fetchall()]
        return index_models

    def put(self, cursor, conn):
        if not self.pickled_index:
            self.pickled_index = pickle.dumps(self.un_pickled_index)
        cursor.execute(
            'INSERT INTO SearchIndex VALUES (?, ?)',
            (self.identifier, self.pickled_index))
        conn.commit()


def search(cursor, conn, query):

    index = load_index(cursor, conn)

    logging.debug('Docs;', len(index))

    words = [x.lower() for x in query.split()]

    logging.debug('End query;', [x for x in words if x not in Document.stopwords])

    logging.debug('Unique indexed words;', len(list(set(chain.from_iterable([x.keys() for x in index.values()])))))

    scores = defaultdict(float)
    for page in index:
        for word in words:
            if word in index[page]:
                scores[page] += index[page][word]

    logging.debug('Relevant pages;', len(scores))

    scores = sorted(scores.items(), key=lambda x: x[1])[::-1]
    return scores


def main():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    conn.execute('DROP TABLE IF EXISTS SearchIndex')
    conn.execute('''
        CREATE TABLE SearchIndex (
            identifier TEXT NOT NULL,
            index_dict BLOB NOT NULL,
            PRIMARY KEY(identifier)
        );''')

    # do the search function
    result = search(cursor, conn, 'gandalf')

    assert sum([x[1] for x in result]) == 0.0, 'assert relevancy works'

    assert len(result) > 0

    conn.close()


if __name__ == '__main__':
    main()
