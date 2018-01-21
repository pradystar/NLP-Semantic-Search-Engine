'''
search index using NLP features
'''

import sys

from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.tag.util import tuple2str
from nltk.stem import PorterStemmer

from indexer import get_semantic_features
from indexer import get_lemmatized_line
from indexer import get_dependency_relations

import pysolr

def search(query, method, instance_url):
    '''
    search solr index using user query
    '''
    q_list = []
    solr = pysolr.Solr(instance_url)
    tokens = word_tokenize(query)
    if method == 1:
        q_list.append('text:' + ' '.join(tokens))
    else:
        stemmer = PorterStemmer()
        tagged_tokens = pos_tag(tokens)
        synonyms, hypernyms, hyponyms, meronyms, holonyms = get_semantic_features(
            tagged_tokens, tokens)
        lemmas = get_lemmatized_line(tagged_tokens)
        head_words = get_dependency_relations(lemmas, True)
        stem_line = [stemmer.stem(t) for t in tokens]
        tagged_list = [tuple2str(t) for t in tagged_tokens]

        pos_tag_data = '&'.join(tagged_list)
        lemmas = '&'.join(lemmas.split())
        stems = '&'.join(stem_line)
        synonyms = '&'.join(synonyms.split())
        hypernyms = '&'.join(hypernyms.split())
        hyponyms = '&'.join(hyponyms.split())
        holonyms = '&'.join(holonyms.split())
        meronyms = '&'.join(meronyms.split())
        head_words = '&'.join(head_words.split())
        if method == 2:
            if tokens:
                q_list.append('text:' + '&'.join(tokens))
            if pos_tag_data:
                q_list.append('pos_tag:' + pos_tag_data)
            if lemmas:
                q_list.append('lemmas:' + lemmas)
            if stems:
                q_list.append('stems:' + stems)
            if synonyms:
                q_list.append('synonyms:' + synonyms)
            if hypernyms:
                q_list.append('hypernyms:' + hypernyms)
            if hyponyms:
                q_list.append('hyponyms:' + hyponyms)
            if meronyms:
                q_list.append('meronyms:' + meronyms)
            if holonyms:
                q_list.append('holonymns:' + holonyms)
            if head_words:
                q_list.append('head_word:' + head_words)
        if method == 3:
            if tokens:
                q_list.append('text:' + '&'.join(tokens) + '^0.5')
            if pos_tag_data:
                q_list.append('pos_tag:' + pos_tag_data + '^0.02')
            if lemmas:
                q_list.append('lemmas:' + lemmas + '^4')
            # if stems:
            #     q_list.append('stems:' + stems + '^1.5')
            if synonyms:
                q_list.append('synonyms:' + synonyms + '4')
            if hypernyms:
                q_list.append('hypernyms:' + hypernyms + '^5')
            # if hyponyms:
            #     q_list.append('hyponyms:' + hyponyms + '^4')
            if head_words:
                q_list.append('head_word:' + head_words + '^0.5')
            # if meronyms:
            #     q_list.append('meronyms:' + meronyms + '^1.4')
            # if holonyms:
            #     q_list.append('holonymns:' + holonyms + '^1.4')
    q_string = ', '.join(q_list)
    print('The Solr query is q=%s, fl=\'id,text\'\n' % (q_string))
    result = solr.search(q=q_string, fl='id,text')
    # for r in json.dumps(result.docs):
    #     print(r)
    for r in result:
        print(r['id'])
        print(' '.join(r['text']))

def main():
    '''
    main function
    '''
    # line = "large mammal gone extinct"
    # line = "stop illegal fishing"
    # line = "spread hiv aids"
    # line = "the School of the Air"
    # line = 'where is rice grown'
    # line = 'largest dinosaur fossil ever found in an excavation site'
    method = int(sys.argv[1])
    instance = 'http://localhost:8983/solr/collection_1/'
    if method == 1:
        print('Performing naive search...')
        instance = 'http://localhost:8983/solr/collection_0/'
    elif method == 2:
        print('Performing deep NLP pipeline search...')
    else:
        print('Performing improved deep NLP pipeline search...')
    line = input('Enter search query: ')
    search(line, method, instance)

if __name__ == '__main__':
    main()
    