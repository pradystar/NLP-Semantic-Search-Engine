'''
This file is specifically created for extracting data for
    Australian Broadcasting Commission 2006
    http://www.abc.net.au/
    Contents:
        * Rural News    http://www.abc.net.au/rural/news/
        * Science News  http://www.abc.net.au/science/news/
'''
from io import StringIO

def main():
    '''
    Read corpus and extract the file.
    '''
    file_id_r = 1
    file_id_s = 1
    str_buf_r = StringIO()
    str_buf_s = StringIO()
    file_r = 'abc/rural.txt'
    file_s = 'abc/science.txt'
    with open(file_r, 'r') as corpus_r, open(file_s, 'r', encoding='iso-8859-15') as corpus_s:
        for line_r, line_s in zip(corpus_r, corpus_s):
            line_strp_r = line_r.strip()
            line_strp_s = line_s.strip()
            if line_strp_r == '':
                with open('extract/r'+ str(file_id_r), 'w+') as out:
                    out.write(str_buf_r.getvalue())
                file_id_r += 1
                str_buf_r = StringIO()
            else:
                str_buf_r.write(line_r)
            if line_strp_s == '':
                with open('extract/s' + str(file_id_s), 'w+') as out:
                    out.write(str_buf_s.getvalue())
                file_id_s += 1
                str_buf_s = StringIO()
            else:
                str_buf_s.write(line_s)

if __name__ == '__main__':
    main()
