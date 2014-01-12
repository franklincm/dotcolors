#!/usr/bin/env python2

import os
import re
import sys
import tempfile
import subprocess

from shutil import move
from os.path import expanduser, exists

home = expanduser('~')
themefile = home + '/.termcolors'
themedir = home + '/.config/termcolors'

def get_current():
    """return current Xresources color theme"""
    if exists(themefile):
        f = open(home + '/.termcolors').read()
        current = re.findall('config[^\s]+', f)[0].split('/')[-1]
        return current
    else:
        return "** Not Set **"

def get_colors():
    """return list of  available Xresources color themes"""
    if exists(themedir):
        contents = os.listdir(themedir)
        themes = [theme for theme in contents if '.' not in theme]
        if len(themes) > 0:
            themes.sort()
            return themes
        else:
            print "**No themes in themedir**"
            sys.exi(0)
    else:
        print "** Theme directory not found **"
        print "First create ~/.config/xresources and place themefiles within."
        sys.exit(0)

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
            menu(get_colors())
            print "Not a valid integer."
    return colors[entry - 1]

def write_changes(current, selection):
    fd, tmpfile = tempfile.mkstemp()

    if exists(themefile):
        old = open(home + '/.termcolors')
        new = os.fdopen(fd, 'w')
        for line in old:
            os.write(fd, line.replace(current, selection))
        old.close()
        new.close()
        move(tmpfile, home + '/.termcolors')

    else:
        new = os.fdopen(fd, 'w')
        os.write(fd, 'xrdb -load ~/.config/xresources/' + selection + '\n')
        os.write(fd, 'xrdb -merge ~/.Xresources\n')
        new.close()
        move(tmpfile, home + '/.termcolors')

    #check for xrdb and apply
    proc = subprocess.Popen(["which", "xrdb"], stdout=subprocess.PIPE)
    tmp = proc.stdout.read()

    if len(tmp) > 0:
        os.system('sh ~/.termcolors')
        print 'Changes applied.'
        print 'Restart terminal for changes to take effect.'
        return
        
    else:
        print '** \'xrdb\' Not Found **\n'
        print 'Install xrdb and try again\n'

    
if __name__ == '__main__':
    try:
        colors = get_colors()
        menu(colors)
        current = get_current()
        selection = get_selection(colors)
        write_changes(current, selection)
        
    except KeyboardInterrupt:
        sys.exit(0)
