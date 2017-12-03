'''
search solr index db using user query
'''
import sys
import json
import pysolr

def search(query, instance_url='http://localhost:8983/solr/collection_1/'):
    '''
    search solr index using user query
    '''
    solr = pysolr.Solr(instance_url)
    result = solr.search(q='text:' + query, fl='id, text, score')
    print(json.dumps(result.docs))

def main():
    '''
    call to search method
    '''
    # method = sys.argv[1]
    search('prime minister')

if __name__ == '__main__':
    main()
