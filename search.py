from nltk.tokenize import word_tokenize
from nltk import pos_tag
from indexer import get_semantic_features
from indexer import get_lemmatized_line
from nltk.tag.util import tuple2str
from nltk.stem import PorterStemmer
import sys
import json
import pysolr

def search(query, instance_url='http://localhost:8983/solr/collection_1/'):
    '''
    search solr index using user query
    '''
    stemmer=PorterStemmer()
    tokens=word_tokenize(query)
    tagged_tokens= pos_tag(tokens)
    synonyms, hypernyms, hyponyms, meronyms, holonyms=get_semantic_features(tagged_tokens,tokens)
    lemmas=get_lemmatized_line(tagged_tokens)
    stem_line = [stemmer.stem(t) for t in tokens]
    stems=' '.join(stem_line)
    tagged_list= [tuple2str(t) for t in tagged_tokens]

    pos_tag_data= ' '.join(tagged_list)
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
    # if query:
    #     q_list.append('text:' + query)
    if pos_tag_data:
        q_list.append('pos_tag:' + pos_tag_data +'^0.02')
    if lemmas:
        q_list.append('lemmas:' + lemmas +'^0.7')
    if stems:
        q_list.append('stems:' + stems +'^0.5')
    if synonyms:
        q_list.append('synonyms:' + synonyms +'^1.5')
    if hypernyms:
        q_list.append('hypernyms:' + hypernyms +'^0.8')
    if hyponyms:
        q_list.append('hyponyms:' + hyponyms +'^0.8')
    if meronyms:
        q_list.append('meronyms:' + meronyms +'^0.8')
    # print(','.join(q_list))
    q_string = ', '.join(q_list)
    result = solr.search(q=q_string , fl='id,text')
    # for r in json.dumps(result.docs):
    #     print(r)
    for r in result:
        print(r['id'], r['text'])
        # print(r['text'])

def main():
    line = "stones in kidney"
    search(line)
if __name__ == '__main__':
    main()
    
    