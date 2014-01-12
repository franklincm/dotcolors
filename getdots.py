#!/usr/bin/env python2
#
# TODO: progress bar, PyPI package
#

from BeautifulSoup import BeautifulSoup
import urllib
from os.path import expanduser

HOME = expanduser('~')
THEMEDIR = HOME + '/.config/xresources/tmp/'

def get_pages():
    '''returns list of urllib file objects'''
    pages =[]
    counter = 1
    while(True):
        page = urllib.urlopen('http://dotshare.it/category/terms/colors/p/%d/' % counter)
        if page.code >= 400:
            break
        pages.append(page)
        counter += 1
    return pages

def get_urls(htmlDoc):
    '''takes in html document as string, returns links to dots'''
    soup = BeautifulSoup( htmlDoc )
    anchors = soup.findAll( 'a' )
    urls = {}

    for i,v in enumerate( anchors ):
        href = anchors[i].get( 'href' )
        if 'dots' in href:
            href = href.split('/')[2]
            text = anchors[i].text.split(' ')[0].replace('/', '_')
            urls[ text ] = href
    return urls

def get_themes(urls):
    '''takes in dict of names and urls, downloads and saves files'''
    
    for i in urls.keys():
        href = 'http://dotshare.it/dots/%s/0/raw/' % urls[i]
        theme = urllib.urlopen(href).read()
        f = open(THEMEDIR + i, 'w')
        f.write(theme)
        f.close()

if __name__ == '__main__':
    
    urls = {}
    p = get_pages()
    for i in p:
        tmp = get_urls(i.read())
        urls.update(tmp)
        
    get_themes(urls)
#    for i in urls.keys():
#        print i,urls[i]
