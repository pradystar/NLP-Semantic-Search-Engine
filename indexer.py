'''
    This file is specifically created to extract the mentioned below details for the words in the corpus:
    -Lemmas
    -Stem 
    -POS tags
    -Using wordnet extract hypernyms, hyponyms, meronyms and holonyms
    -Syntactically parse the sentence, extract phrases, head words, dependency parse relations
'''
import os   
import sys
import pysolr
import string
from nltk.stem.porter import *
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk import word_tokenize
from nltk.tag.util import tuple2str

#solr = pysolr.Solr('http://localhost:8983/solr/main_core', timeout=10)

def processing_data():
    '''
        Extracting the data as per the requirements.
    '''
    path = "extract_test"
    dirs= os.listdir(path)
    for f in dirs:
        with open('extract_test/'+f,'r') as curr_file:
            for line in curr_file:
                for c in string.punctuation:
                    line=line.replace(c,"")
    
                word_vector = []
                lemmatize_sentence = ''
                stemmed_sentence = ''
                pos_tag_sentence = ''
                hyper_data=''
                hypo_data=''
                meronym_data='' 
                word_vector = word_tokenize('PM denies knowledge of AWB kickbacks', language='english')
                pos_tag_sentence = func_pos_tagg(word_vector)
                #print(pos_tag_sentence)
                pos_word_vector= pos_tag_sentence.split()
                lemmatize_sentence = func_lemmatize(pos_word_vector)
                #print(lemmatize_sentence)
                stemmed_sentence= func_stemmer(word_vector)
                #print ("Stemmed Sentence: "+stemmed_sentence)
                hyper_data=func_hypernym(word_vector)
                #print(hyper_data)
                hypo_data=func_hyponym(word_vector)
                #print(hypo_data)
                meronym_data=func_meronym(word_vector)
                #print(meronym_data)

def func_lemmatize(sentence_words):
    '''
        Function to lemmatize the sentence words.Lemma's will be found for noun, adverb, adjective and adverb.
        ** change string to list
    '''
    wnl = WordNetLemmatizer()
    lemma_list = []
    lemmas = ''
    tag=''
    for w in sentence_words:
        word_lemmas = ''
        wrd=(w).split('/')[0]
        tag_data= (w).split('/')[1]
        tag=find_tag(wrd,tag_data)
        if (tag !=''):
            word_lemmas=wrd 
            data = wnl.lemmatize(wrd, tag)
            word_lemmas = word_lemmas+" "+data+" "
        lemma_list.append(word_lemmas)
    lemmas = ''.join(lemma_list)
    return lemmas

def find_tag(wrd,tag_data):
    '''
        This function determines the tag, which is used by the wordNetLemmatizer to determine the lemma.
    '''  
    tag=''
    if tag_data.startswith('N'):
        tag = 'n'
    elif tag_data.startswith('J'):
        tag= 'a'
    elif tag_data.startswith('R'):
        tag= 'r'
    elif tag_data.startswith('V'):
        tag='v' 
    return tag

def func_stemmer(sentence_words):
    '''
        Function to stem the sentence words.
    '''
    pt = PorterStemmer()
    word_stems = ''
    for w in sentence_words:
        stem_word = ''
        w_1 = w.lower()
        stem_word = pt.stem(w_1)
        word_stems = word_stems+" " +stem_word 
    return word_stems


def func_pos_tagg(sentence_words):
    '''
        Function to tag the words of the sentence.
        ** change it to list**
    '''
    tagged_sentence = ''
    formatted_sentence= ''
    tagged_sentence = pos_tag(sentence_words)
    for tagged_token in tagged_sentence:
        formatted_sentence= formatted_sentence+" "+tuple2str(tagged_token)
    return formatted_sentence

def func_hypernym(sentence_words):
    '''
        This function determines the hypernyms for the words of the sentence, by first determining the synsets.
    '''
    hyper_words=''
    for words in sentence_words: 
        for synset in wordnet.synsets(words):
            syn_hyper=''
            hyper_details=[]
            hyper_details_data=''
            if str(synset.hypernyms())=='[]':
                hyper_details.append(words)
            else:
                hyper_details.append(str(synset.hypernyms()))      
            hyper_details_data=' '.join(hyper_details)
            syn_hyper=syn_hyper+' '+hyper_details_data+' '
            hyper_words=hyper_words+''+syn_hyper
    return hyper_words

def func_hyponym(sentence_words):
    '''
        This function determines the hyponyms for the words of the sentence, by first determining the synsets.
    '''
    hypo_words=''
    hypo_details=set()
    for words in sentence_words:
        for synset in wordnet.synsets(words):
            if str(synset.hyponyms())== []:
                hypo_details.add(words)
            else:
                hypo_details.add(str(synset.hyponyms()))
        hypo_words=' '.join(hypo_details)
    return hypo_words 

def func_meronym(sentence_words):
    '''
        This function determines the meronyms for the words of the sentence, by first determining the synsets.
    '''
    meronym_words=''
    meronym_details=set()
    for words in sentence_words:
        for synset in wordnet.synsets(words):
            data=str(synset.part_meronyms())
            if data!='[]':
                meronym_details.add(data)
            else:
                meronym_details.add(words)
        meronym_words=' '.join(meronym_details)
    return meronym_words


def main():
    processing_data()


if __name__ == "__main__":
    main()
