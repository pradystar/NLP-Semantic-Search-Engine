'''
Index data into solr
'''
from os import listdir
import time
import sys

from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk.stem.porter import PorterStemmer
from nltk.tag.util import tuple2str
from nltk.stem.wordnet import WordNetLemmatizer
# from nltk.parse.corenlp import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
# from nltk.parse.stanford import StanfordParser as sp
# from nltk.parse.stanford import StanfordDependencyParser as sdp

import pysolr
# nltk pos tag to wordnet tag map
WN_TAG_LIST = {
    'NN': wn.NOUN,
    'VB': wn.VERB,
    'JJ': wn.ADJ,
    'RB': wn.ADV
    }

# initialize dependenices for StanfordDependency Parse
# STANFORD_VER = 'stanford-corenlp-3.8.0'
# PATH_TO_JAR = 'jars/stanford-corenlp/' + STANFORD_VER + '.jar'
# PATH_TO_MODELS_JAR = 'jars/stanford-corenlp/' + STANFORD_VER + '-models.jar'
# STANFORD_DEP_PARSER = sdp(path_to_jar=PATH_TO_JAR, path_to_models_jar=PATH_TO_MODELS_JAR)
# STANFORD_PARSER = sp(path_to_jar=PATH_TO_JAR, path_to_models_jar=PATH_TO_MODELS_JAR)

# CONLP = CoreNLPParser()
CONLDP = CoreNLPDependencyParser()

def get_semantic_features(tagged_tok, line):
    '''
    return features like synonyms, hypernyms, hyponyms, meronyms, holonymns
    extracted from each word of sentence
    '''
    # use synset or enumerate??
    lemma_sen = set()
    hyper_sen = set()
    hypo_sen = set()
    mero_sen = set()
    holo_sen = set()
    for word, tag in tagged_tok:
        if tag[:2] in WN_TAG_LIST:# and tag != 'NNP':
            # sense = lesk(line, word, pos=WN_TAG_LIST.get(tag[:2]))
            sense = lesk(line, word)
            if not sense:
                continue
            for lem in sense.lemmas():
                lemma_sen.add(lem.name())
            for hyper in sense.hypernyms()[:30]:
                hyper_sen.add(hyper.name())
            for hypo in sense.hyponyms()[:30]:
                hypo_sen.add(hypo.name())
            for mero in sense.part_meronyms()[:30]:
                mero_sen.add(mero.name())
            for holo in sense.member_holonyms()[:30]:
                holo_sen.add(holo.name())
    return (' '.join(lemma_sen), ' '.join(hyper_sen), ' '.join(hypo_sen),
            ' '.join(mero_sen), ' '.join(holo_sen))

def get_lemmatized_line(tagged_tok):
    '''
    return lemmatized string
    '''
    wnl = WordNetLemmatizer()
    lemma_list = []
    for word, tag in tagged_tok:
        if tag[:2] in WN_TAG_LIST:
            word = wnl.lemmatize(word, pos=WN_TAG_LIST.get(tag[:2]))
        lemma_list.append(word)
    return ' '.join(lemma_list)

def get_dependency_relations(line, q=False):
    '''
    extract dependency tree and head word of the sentence
    '''
    # result = STANFORD_DEP_PARSER.raw_parse(line)
    # parse_result = STANFORD_PARSER.raw_parse(line)
    head_words = set()
    result = CONLDP.raw_parse(line)
    dep_tree = [r for r in result]
    # parse_result = CONLP.raw_parse(line)
    # parse_tree = [r for r in parse_result]
    # print(dep_tree)
    dep_dict = dep_tree[0]
    root_word = dep_dict.root['word']
    # print(head)
    for head, _, _ in dep_dict.triples():
        head_words.add(head[0])
    if q:
        return ' '.join(head_words)
    if root_word in head_words:
        head_words.remove(root_word)
    head_words.add(root_word + '^2')
    # noun_phrases_list = []
    # verb_phrases_list = []
    # for subtree in parse_tree[0].subtrees(filter=lambda x: x.label() in ('NP', 'VP')):
    #     if subtree.label() == 'NP':
    #         noun_phrases_list.append(' '.join(subtree.leaves()))
    #     else:
    #         verb_phrases_list.append(' '.join(subtree.leaves()))
    return ' '.join(head_words)#, ' '.join(noun_phrases_list), ' '.join(verb_phrases_list)

def indexer(instance_url='http://localhost:8983/solr/collection_1/', dir_file='extract', method=1):
    '''
    load the solr instace and index from the dir_file
    '''
    start = time.time()
    solr = pysolr.Solr(instance_url)
    files = listdir(dir_file)
    tot = len(files)
    counter = 0
    data = []
    stemmer = PorterStemmer()
    for f in files:
        counter += 1
        # print(counter)
        sentence_id = 0
        first = True
        with open('extract/' + f, 'r') as doc:
            for line in doc:
                sentence_id += 1
                if first:
                    first = False
                    title = line.strip()
                    # continue
                line = line.strip()
                tokens = word_tokenize(line)
                if method == 0:
                    data.append({
                        'id': f + '_' + str(sentence_id),
                        'title': title,
                        'text': ' '.join(tokens),
                    })
                    continue
                tagged_tok = pos_tag(tokens)
                tagged_list = [tuple2str(t) for t in tagged_tok]
                lemma_line = get_lemmatized_line(tagged_tok)
                stem_line = [stemmer.stem(t) for t in tokens]
                # head_word, noun_phrases, verb_phrases = get_dependency_relations(lemma_line)
                head_word = get_dependency_relations(lemma_line)
                synonyms, hypernyms, hyponyms, meronyms, holonymns = get_semantic_features(
                    tagged_tok, tokens)
                data.append({
                    'id': f + '_' + str(sentence_id),
                    'title': title,
                    'text': ' '.join(tokens),
                    'pos_tag': ' '.join(tagged_list),
                    'lemmas': lemma_line,
                    'stems': ' '.join(stem_line),
                    'synonyms': synonyms,
                    'hypernyms': hypernyms,
                    'hyponyms': hyponyms,
                    'meronyms': meronyms,
                    'holonymns': holonymns,
                    'head_word': head_word,
                    # 'noun_phrases': noun_phrases,
                    # 'verb_phrases': verb_phrases
                })
                # sentence_id += 1
        if counter % 1000 == 0:
            print('processed %d/%d' %(counter, tot))
            solr.add(data)
            data = []
    if data:
        solr.add(data)
    print(time.time() - start)

def main():
    '''
    call indexer
    '''
    # files = [f for f in listdir('extract')]
    # print(files)
    # indexer()
    if int(sys.argv[1]) == 0:
        indexer(instance_url='http://localhost:8983/solr/collection_0/', method=0)
    else:
        indexer()
    # print(get_dependency_relations('Snowy Hydro inquiry wo n\'t delay sale'))

if __name__ == '__main__':
    main()
