# -*- coding: utf-8 -*-

import math
import os
import re
import sys
import subprocess
import tempfile

from utils import _Getch
from utils import raw_input_with_default
from utils import rgb_to_hex
from utils import hex_to_rgb
from utils import decimal_to_alpha

from shutil import move
from os.path import expanduser
from os.path import exists

from StringIO import StringIO

HOME = expanduser('~')
SETTINGSFILE = HOME + '/.dotcolorsrc'
XRESOURCES = HOME + '/.Xresources'
THEMEDIR = HOME + '/.config/dotcolors'

#background = None
transparency = 100
themefile = ''
prefix = 'urxvt'
current = ''

def get_current():
    """return current Xresources color theme"""
    global current
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
(j/k): Next/Previous page, (J/K): Transparency Down/Up

(P/p): set prefix,         (Q/q): Quit

Or simply enter the number of a theme
    """

    print '=' * 30
    print page_display
    print '-' * len(page_display)

    for i,v in enumerate(colors[start : start + per_page]):
        print '%2d) %s' % (i + start + 1, v)

    print '=' * 30
    print 'Current theme is: %s' % get_current()
    print 'Transparency: %%%d' % transparency
    print '=' * 30

    if(print_keys):
        print keys


def getch_selection(colors, per_page=15):
    """prompt for selection, validate input, return selection"""
    global transparency, prefix, current
    get_transparency()
    
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

        if( char == 'j' ):
            page += 1
            if page > last_page:
                page = last_page
            menu_pages(colors, page, True, per_page)


        if( char == 'k' ):
            if(page > 1):
                page -= 1
            else:
                page = 1
            menu_pages(colors, page, True, per_page)


        if( char.lower() == 'q' ):
            c = os.system('clear')
            sys.exit(0)

        if( char == 'J' ):
            if transparency > 0:
                transparency -= 1
            menu_pages(colors, page, True, per_page)

        if( char == 'K' ):
            if transparency < 100:
                transparency += 1
            menu_pages(colors, page, True, per_page)

        if( char.lower() == 'p' ):
            prefix = raw_input_with_default(' prefix: ', 'urxvt')
            
        if( char == '\r' ):
            return current

    return colors[entry - 1]


def format_theme(selection):
    """removes any non-color related lines from theme file"""
    global themefile

    text = open(THEMEDIR + '/' + selection).read()
    if '!dotcolors' in text[:10]:
        themefile = text
        return

    lines = ['!dotcolors auto formatted\n']
    for line in text.split('\n'):
        lline = line.lower()
        background = 'background' in lline
        foreground = 'foreground' in lline
        color = 'color' in lline

        if background:
            if 'rgb' in line:
                # rbga: 0000/0000/0000/dddd
                rgb = line.split(':')[2].replace(' ', '')
                rgb = rgb_to_hex(rgb)
                lines.append('*background:\t%s' % rgb)
            else:
                lines.append('\t#'.join(line \
                                        .replace(' ', '') \
                                        .replace('\t', '') \
                                        .split('#')))

        if foreground:
            if 'rgb' in line:
                # rbga: 0000/0000/0000/dddd
                rgb = line.split(':')[2].replace(' ', '')
                rgb = rgb_to_hex(rgb)
                lines.append('*foreground:\t%s' % rgb)
            else:
                lines.append('\t#'.join(line \
                                        .replace(' ', '') \
                                        .replace('\t', '') \
                                        .split('#')))

        if color:
            if lline[0] != '!':
                lines.append('\t#'.join(line \
                                        .replace(' ', '') \
                                        .replace('\t', '') \
                                        .split('#')))
    
    themefile = '\n'.join(lines) + '\n'
    fd, tmpfile = tempfile.mkstemp()
    if exists( THEMEDIR + '/' + selection ):
        old = open( THEMEDIR + '/' + selection )
        new = os.fdopen(fd, 'w')
        os.write(fd, themefile)
        old.close()
        new.close()
        move( tmpfile, THEMEDIR + '/' + selection )


def get_transparency():
    global transparency
    try:
        infile = open( XRESOURCES )
        for line in infile:
            if 'rgba' in line:
                alpha = line.split(':')[2].split('/')[3]
                break
    except:
        alpha = 'ffff'
    transparency = math.ceil((int(alpha, 16) / 65535.) * 100)


def write_transparency(selection):
    """writes transparency as rgba to ~/.Xresources"""
    global themefile, transparency, prefix

    if themefile == "":
        return

    lines = themefile.split('\n')

    for line in lines:
        if 'background' in line.lower():
            try:
                background = line.split(':')[1].replace(' ', '')
                background = background.replace('\t', '')
                break
            except:
                msg = ('Cannot determine background color from themefile. '
                       'Defaulting to: #000000')
                print msg
                background = '#000000'
                break
        else:
            background = '#000000'

    background = hex_to_rgb(background)

    fd, tmpfile = tempfile.mkstemp()
    if exists( XRESOURCES ):
        old = open( XRESOURCES )
        new = os.fdopen(fd, 'w')
        for line in old:
            lline = line.lower()

            if 'depth' in lline:
                continue

            elif 'rgba' in lline:
                continue

            elif line == '\n':
                continue

            else:
                os.write(fd, line)

        os.write(fd, '\n%s.depth:\t32' % prefix)
        os.write(fd, '\n%s.background:\trgba:%s/%s\n' %
                 (prefix, background, decimal_to_alpha(transparency)))
        old.close()
        new.close()
        move( tmpfile, XRESOURCES )


def write_changes(current, selection, test):
    if test == False:

        format_theme(selection)
        write_transparency(selection)

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
            os.write(fd, 'xrdb -load ~/.config/dotcolors/' + selection + '\n')
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
#        get_transparency()
        colors = get_colors()
        current = get_current()
        selection = getch_selection(colors, 20)
#        print selection
#        format_theme(selection)
#        write_transparency(selection)
        write_changes(current, selection, False)

    except KeyboardInterrupt:
        sys.exit(0)
