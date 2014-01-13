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
        f = open( HOME + '/.termcolors' ).read()
        current = re.findall('config[^\s]+', f)[0].split('/')[-1]
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
            sys.exit(0)
    else:
        print "** Theme directory not found **"
        print "First create ~/.config/xresources and place themefiles within."
        sys.exit(0)


def menu_pages(colors, page=1):
    """return menu items by page from list: colors"""
    c = os.system('clear')
    print '=' * 25
    start = 25 * (page - 1)
    for i,v in enumerate(colors[start:start+25]):
        print '%2d) %s' % (i+start+1, v)
    print '=' * 25
    print 'Current theme is: %s\n' % get_current()


def menu(colors):
    """return menu items from list: colors """
    c = os.system('clear')
    print '=' * 25
    for i,v in enumerate(colors):
        print '%2d) %s' % (i+1, v)
    print '=' * 25
    print 'Current theme is: %s\n' % get_current()

def get_selection(colors):
    """prompt for selection, validate input, return selection"""
    page = 1
    menu_pages(colors, page)
    valid = False
    while valid == False:
        entry = raw_input("Enter number of selection: ")
        try:
            entry = int(entry)
            if colors[entry - 1]:
                valid = True
        except:
            if type(entry) == type('str'):
                if entry.lower() == 'q':
                    c = os.system('clear')
                    sys.exit(0)
                elif entry.lower() == 'n':
                    page += 1
                    menu_pages(get_colors(), page)
                elif entry.lower() == 'p':
                    if page > 1:
                        page -= 1
                    else:
                        page = 1
                    menu_pages(get_colors(), page)
                else:
                    menu_pages(get_colors())
                    print "Not a valid integer."
    return colors[entry - 1]

def write_changes(current, selection):
    fd, tmpfile = tempfile.mkstemp()

    if exists( SETTINGSFILE ):
        old = open( HOME + '/.termcolors' )
        new = os.fdopen(fd, 'w')
        for line in old:
            os.write(fd, line.replace(current, selection))
        old.close()
        new.close()
        move( tmpfile, HOME  + '/.termcolors' )

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
        os.system('sh ' + SETTINGSFILE)
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
        selection = get_selection(colors)
        write_changes(current, selection)
        
    except KeyboardInterrupt:
        sys.exit(0)
