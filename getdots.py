#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# TODO: replace BeautifulSoup with re
#

import urllib
import sys

from BeautifulSoup import BeautifulSoup
from os.path import expanduser

from progressbar import Percentage
from progressbar import Bar
from progressbar import ETA
from progressbar import ProgressBar
from progressbar import AnimatedMarker


HOME = expanduser('~')
RCFILE = HOME + '/.termcolorsrc'
THEMEDIR = HOME + '/.config/termcolors/'


def get_pages():
    '''returns list of urllib file objects'''
    pages =[]
    counter = 1

    print "Checking for themes..."

    while(True):
        page = urllib.urlopen('http://dotshare.it/category/terms/colors/p/%d/' % counter)
        print "Page%d:  %s" % (counter, "OK" if (page.code < 400) else "Fail!")
        if page.code >= 400:
            break
        pages.append(page)
        counter += 1

    print "Found %d pages." % (counter - 1)
    return pages


def get_urls(htmlDoc, limit=200):
    '''takes in html document as string, returns links to dots'''
    soup = BeautifulSoup( htmlDoc )
    anchors = soup.findAll( 'a' )
    urls = {}

    counter = 0
    for i,v in enumerate( anchors ):
        href = anchors[i].get( 'href' )
        if 'dots' in href and counter <= limit:
            href = href.split('/')[2]
            text = anchors[i].text.split(' ')[0].replace('/', '_')
            urls[ text ] = href
            counter += 1
    return urls


def get_themes(urls):
    '''takes in dict of names and urls, downloads and saves files'''
    
    counter = 1
    widgets = ['Fetching themes: ', Percentage(), ' ', 
               Bar(marker='-'), ' ', ETA()]

    pbar = ProgressBar( widgets=widgets, maxval=len(urls) ).start()

    for i in urls.keys():
        href = 'http://dotshare.it/dots/%s/0/raw/' % urls[i]
        theme = urllib.urlopen(href).read()
        f = open(THEMEDIR + i, 'w')
        f.write(theme)
        f.close()
        pbar.update(counter)
        counter += 1

    pbar.finish()


def run(limit=200):
    try:
        urls = {}
        pages = get_pages()
        for i in pages:
            tmp = get_urls(i.read(), limit)
            if len(urls) < limit:
                urls.update(tmp)
        
        get_themes(urls)
    
    except KeyboardInterrupt:
        print "\n"
        sys.exit(0)

if __name__ == '__main__':
    run(limit)
