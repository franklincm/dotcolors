#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import tempfile
import subprocess

from getch import _Getch
from shutil import move
from os.path import expanduser
from os.path import exists

HOME = expanduser('~')
SETTINGSFILE = HOME + '/.termcolorsrc'
THEMEDIR = HOME + '/.config/termcolors'


def get_current():
    """return current Xresources color theme"""
    if exists( SETTINGSFILE ):
        f = open( SETTINGSFILE ).read()
        current = re.findall('config[^\s]+.+', f)[1].split('/')[-1]
        return current
    else:
        return "** Not Set **"

def get_colors():
    """return list of  available Xresources color themes"""
    if exists( THEMEDIR ):
        contents = os.listdir( THEMEDIR )
        themes = [theme for theme in contents if '.' not in theme]
        if len(themes) > 0:
            themes.sort()
            return themes
        else:
            print "** No themes in themedir **"
            print "    run:"
            print "        termcolors (-s | --sync) <limit>"
            sys.exit(0)
    else:
        print "** Theme directory not found **"
        print "    run: "
        print "        termcolors --setup"


        sys.exit(0)


def menu_pages(colors, page=1, print_keys=True, results_per_page=25):
    """return menu items by page from list: colors"""
    c = os.system('clear')
    print '=' * 25

    start = results_per_page * (page - 1)

    for i,v in enumerate(colors[start:start+results_per_page]):
        print '%2d) %s' % (i+start+1, v)
    print '=' * 25
    print 'Current theme is: %s' % get_current()
    
    keys = """
    N (n) - Next Page
    P (p) - Previous Page
    S (s) - Make Selection
    Q (q) - Quit
    """
    if(print_keys):
        print keys


def getch_selection(colors, results_per_page):
    """prompt for selection, validate input, return selection"""
    page = 1
    length = len(colors)
    last_page = length / results_per_page
    
    if (last_page * results_per_page) < length:
        last_page += 1

    getch = _Getch()

    valid = False
    while valid == False:
        menu_pages(colors, page, True, results_per_page)

        char = getch()
        
        if( char.lower() == 'n' ):
            page += 1
            if page > last_page:
                page = last_page
            menu_pages(colors, page, True, results_per_page)


        if( char.lower() == 'p' ):
            if(page > 1):
                page -= 1
            else:
                page = 1
            menu_pages(colors, page, True, results_per_page)


        if( char.lower() == 's' ):
            entry = raw_input("Enter number of selection: ")
            try:
                entry = int(entry)
                if colors[entry - 1]:
                    valid = True

            except:
                menu_pages(colors, page, True, results_per_page)
                print "Not a valid integer."
                raw_input()

        if( char.lower() == 'q' ):
            c = os.system('clear')
            sys.exit(0)

    sys.stdout.flush()
    return colors[entry - 1]


def write_changes(current, selection, test):
    if test == False:
        fd, tmpfile = tempfile.mkstemp()

        if exists( SETTINGSFILE ):
            old = open( SETTINGSFILE )
            new = os.fdopen(fd, 'w')
            for line in old:
                os.write(fd, line.replace(current, selection))
            old.close()
            new.close()
            move( tmpfile, SETTINGSFILE )

        else:
            new = os.fdopen(fd, 'w')
            os.write(fd, 'xrdb -load ~/.config/xresources/' + selection + '\n')
            os.write(fd, 'xrdb -merge ~/.Xresources\n')
            new.close()
            move( tmpfile, HOME + '/.termcolors' )

    #check for xrdb and apply
    proc = subprocess.Popen(["which", "xrdb"], stdout=subprocess.PIPE)
    tmp = proc.stdout.read()

    if len(tmp) > 0:
        os.system('xrdb -load %s/%s' % (THEMEDIR, selection))
        os.system('xrdb -merge %s/.Xresources' % HOME)
        
        print 'Changes applied.'
        print 'Restart terminal for changes to take effect.'
        return
        
    else:
        print '** \'xrdb\' Not Found **\n'
        print 'Install xrdb and try again\n'

    
if __name__ == '__main__':
    try:
        colors = get_colors()

        current = get_current()
        selection = getch_selection(colors, 26)
        print selection
#        write_changes(current, selection)
        
    except KeyboardInterrupt:
        sys.exit(0)
