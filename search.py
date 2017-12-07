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

def search(query, instance_url='http://localhost:8983/solr/collection_1/'):
    '''
    search solr index using user query
    '''
    stemmer = PorterStemmer()
    tokens = word_tokenize(query)
    tagged_tokens = pos_tag(tokens)
    synonyms, hypernyms, hyponyms, meronyms, holonyms = get_semantic_features(tagged_tokens, tokens)
    lemmas = get_lemmatized_line(tagged_tokens)
    head_words = get_dependency_relations(lemmas)
    stem_line = [stemmer.stem(t) for t in tokens]
    stems = ' '.join(stem_line)
    tagged_list = [tuple2str(t) for t in tagged_tokens]

    pos_tag_data = ' '.join(tagged_list)
    # print('text:' + query, ',pos_tag:'+ pos_tag_data, ',lemmas:'+lemmas, ',stems:'+stems,
    # ',synonyms:'+synonyms, ',hypernyms:'+hypernyms, ',hyponyms:'+hyponyms,'holonymns:'+holonyms)
    solr = pysolr.Solr(instance_url)
    query = '&'.join(query.split())
    pos_tag_data = '&'.join(pos_tag_data.split())
    lemmas = '&'.join(lemmas.split())
    stems = '&'.join(stems.split())
    synonyms = '&'.join(synonyms.split())
    hypernyms = '&'.join(hypernyms.split())
    hyponyms = '&'.join(hyponyms.split())
    holonyms = '&'.join(holonyms.split())
    meronyms = '&'.join(meronyms.split())
    q_list = []
    if query:
        q_list.append('text:' + query + '^0.5')
    if pos_tag_data:
        q_list.append('pos_tag:' + pos_tag_data + '^0.02')
    if lemmas:
        q_list.append('lemmas:' + lemmas + '^3')
    # if stems:
    #     q_list.append('stems:' + stems + '^1.5')
    if synonyms:
        q_list.append('synonyms:' + synonyms + '^3')
    if hypernyms:
        q_list.append('hypernyms:' + hypernyms + '^4')
    if hyponyms:
        q_list.append('hyponyms:' + hyponyms + '^4')
    if 
    # if meronyms:
    #     q_list.append('meronyms:' + meronyms + '^1.4')
    # if holonyms:
    #     q_list.append('holonymns:' + holonyms + '^1.4')
    # print(','.join(q_list))
    q_string = ', '.join(q_list)
    print(q_string)
    result = solr.search(q=q_string, fl='id,text')
    # for r in json.dumps(result.docs):
    #     print(r)
    for r in result:
        print(r['id'])
        print(r['text'])

def main():
    '''
    main function
    '''
    # line = "large mammal gone extinct"
    # line = "stop illegal fishing"
    # line = "spread hiv aids"
    # line = "the School of the Air"
    line = 'where is rice grown'
    line = 'largest dinosaur fossil ever found in an excavation site'
    search(line)

if __name__ == '__main__':
    main()
    