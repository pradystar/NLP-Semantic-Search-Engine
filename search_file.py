import pysolr
import os
import re
solr = pysolr.Solr('http://localhost:8983/solr/new_core', timeout=10)

'''
    This file is created for searching the data indexed in solr by index_file.py file, which indexed the data of Austrailian Broadcasting
    Comission 2006.
    Input: Data to be queried, to be entered by the user.
    Output: Matched sentences and their respective scores. Top 10 search results with the maximum score are processed.
'''

# This function implements the search fumction in solr.

def search_data(query):
    result = solr.search(q='text:' + query, fl='id,text_str,score',)
    result_list = []
    for r in result:
        r_score_list = str(r).split('score')
        r_score = 'score' + str(r_score_list[1]).strip(':\'}')
        data = re.search("\[.*\]", str(r))
        result_data = r_score + ": " + \
            data.group(0).replace('[\'', '').replace(
                '\']', '').replace('\\n', '')
        result_list.append(result_data)
    if (len(result_list) > 10):
        r_list = []
        for i in range(10):
            r_list.append(result_list[i])
        return r_list
    else:
        return result_list

    return

# main function.

def main():
    data = input('Please enter the data to be searched: ')
    res_list = []
    res_list = search_data(data)
    for r in res_list:
        print(r)


if __name__ == "__main__":
    main()
