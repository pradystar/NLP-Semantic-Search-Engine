import os
import glob
import nltk
import pysolr
from nltk.tokenize import word_tokenize
from nltk import word_tokenize

'''
    This file is created to index the data present in the files created by the file extract.py, uses the indexing feature of solr-7.1.0.
    The unique id provided to the files is a cobination of  the file name and the sentence id.
'''

solr = pysolr.Solr('http://localhost:8983/solr/new_core', timeout=10)

# This function indexes the data, iterating through the files.

def index_file():
    path = "extract\\*"
    global solr
    for file_name in glob.glob(path):
        sentence_id = 1
        with open(file_name) as f:
            for lines in f:
                name = file_name.split('extract\\')
                f_name = name[1]
                solr.add([{"id": str(f_name) + "_" + str(sentence_id),
                           "text": str(lines), }])
                sentence_id += 1
# main function

def main():
    index_file()


if __name__ == "__main__":
    main()
