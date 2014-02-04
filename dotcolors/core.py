# -*- coding: utf-8 -*-

import os
import re
import sys
import tempfile
import subprocess

from utils import _Getch
from utils import raw_input_with_default
from shutil import move
from os.path import expanduser
from os.path import exists

from StringIO import StringIO

HOME = expanduser('~')
SETTINGSFILE = HOME + '/.dotcolorsrc'
THEMEDIR = HOME + '/.config/dotcolors'


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
            print "        dotcolors (-s | --sync) <limit>"
            sys.exit(0)
    else:
        print "** Theme directory not found **"
        print "    run: "
        print "        dotcolors --setup"


        sys.exit(0)


def menu_pages(colors, page=1, print_keys=True, per_page=15):
    """return menu items by page from list: colors"""

    c = os.system('clear')

    length = len(colors)
    last_page = length / per_page
    if (last_page * per_page) < length:
        last_page += 1

    page_display = "page (%d/%d)" % (page, last_page)

    start = per_page * (page - 1)

    keys = """
(j/J) Next page,  (k/K) Previous page,  (Q)uit
Or simply enter the number of a theme
    """

    print '=' * 30
    print page_display
    print '-' * len(page_display)

    for i,v in enumerate(colors[start : start + per_page]):
        print '%2d) %s' % (i + start + 1, v)

    print '=' * 30
    print 'Current theme is: %s' % get_current()
    print '=' * 30

    if(print_keys):
        print keys


def getch_selection(colors, per_page=15):
    """prompt for selection, validate input, return selection"""
    page = 1
    length = len(colors)
    last_page = length / per_page

    if (last_page * per_page) < length:
        last_page += 1

    getch = _Getch()

    valid = False
    while valid == False:
        menu_pages(colors, page, True, per_page)
        sys.stdout.write(">")
        char = getch()

        try:
            int(char)
            entry = raw_input_with_default(' Selection: ', char)
            entry = int(entry)
            if colors[entry - 1]:
                valid = True

        except ValueError:
            pass

        if( char.lower() == 'j' ):
            page += 1
            if page > last_page:
                page = last_page
            menu_pages(colors, page, True, per_page)


        if( char.lower() == 'k' ):
            if(page > 1):
                page -= 1
            else:
                page = 1
            menu_pages(colors, page, True, per_page)


        if( char.lower() == 'q' ):
            c = os.system('clear')
            sys.exit(0)

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
            move( tmpfile, HOME + '/.dotcolorsrc' )

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
