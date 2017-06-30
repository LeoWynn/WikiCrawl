#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
#Module:wiki_crawl.py
#Created by Leo Wen
'''

import re
import urllib2

class WikiCrawl(object):
    '''
    #WikiCrawl
    '''
    def __init__(self):
        '''Init class'''
        self.wiki_url = 'https://en.wikipedia.org/wiki/Machine_translation'
        self.year_length = 4
        self.html_name = ''

    def _crawl_wiki_webpage(self):
        '''Crawl wiki webpage(html) by wiki url
        Return html
        '''
        html = urllib2.urlopen(self.wiki_url).read()
        return html

    def save_html(self, html_name):
        '''Save html '''
        self.html_name = html_name
        html = self._crawl_wiki_webpage()
        file_id = open(self.html_name, 'w')
        file_id.write(html)
        file_id.close()

    def _read_html_file(self):
        '''Read html info from a .html file.
        Return html
        '''
        file_id = open(self.html_name, 'r')
        html = file_id.read()
        return html

    @staticmethod
    def _parser_words(html):
        '''Crawl all content from <p>
        Parser all words, and count the same word
        Return count_word
        '''
        words_list = []
        crawl_content = re.findall(r'<p>(.*?)</p>', html)
        for item in crawl_content:
            for word in re.findall(r'[a-zA-Z]{1,}', item):
                words_list.append(word)
        words_list.sort()

        #Count the same word
        count_word = []
        count = 0
        word = None
        for val in words_list:
            if word is None:
                word = val
                count = 1
            else:
                if word == val:
                    count += 1
                else:
                    count_word.append([count, word])
                    word = val
                    count = 1
        count_word.append([count, word])
        count_word.sort()
        #print count_word
        return count_word

    def save_words(self, file_name):
        '''Save all words and count to file'''
        html = self._read_html_file()
        count_word = self._parser_words(html)
        file_id = open(file_name, 'w')
        for item in count_word:
            file_id.write(item[1] + '\t' + str(item[0]) + '\n')
        file_id.close()

    def _parser_years(self, html):
        '''Parser all years from html'''
        years_list = []
        for item in re.findall(r'[0-9]{4,}', html):
            if len(item) == self.year_length:
                years_list.append(item)
        years_set = set(years_list)
        years_list = list(years_set)
        years_list.sort()
        return years_list

    def save_years(self, file_name):
        '''Save all year to file'''
        html = self._read_html_file()
        years_list = self._parser_years(html)
        file_id = open(file_name, 'w')
        for year in years_list:
            file_id.write(str(year) + '\n')
        file_id.close()

def test():
    '''Test WikiCrawl class '''
    wiki_crawl = WikiCrawl()
    wiki_crawl.save_html('./mt.html')
    wiki_crawl.save_words('./mt_word.txt')
    wiki_crawl.save_years('./mt_year.txt')


if __name__ == "__main__":
    test()
