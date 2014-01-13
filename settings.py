#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import makedirs
from os import listdir
from os.path import expanduser
from os.path import exists
from os.path import isdir

import re

HOME = expanduser('~')
RCFILE = HOME + '/.termcolorsrc'
#THEMEDIR = HOME + '/.config/termcolors/'

TEXT = """
#!/bin/sh
#
# ~/.termcolorsrc
#
# Add this to your .xinitrc or .xprofile:
#
#    sh ~/.termcolorsrc
#

termcolors_THEMEDIR='~/.config/termcolors/'

xrdb -load %s** Not Set **
xrdb -merge ~/.Xresources 

""" % (THEMEDIR)


def set_rcfile():
    if(exists( RCFILE )):
        return
    else:
        outfile = open( RCFILE, 'w')
        outfile.write( TEXT )
        outfile.close()

def gset_themes_dir():
    if(exists( RCFILE )):
        infile = open( RCFILE ).read()
        themes_dir = re.findall('termcolors_THEMEDIR[^\s]+', infile)[0].split("'")[1]
        if( len(themes_dir) > 0 ):
            themes_dir = expanduser( themes_dir )
        else:
            themes_dir = expanduser( "~/.config/termcolors/" )


        if(isdir( themes_dir )):
            return themes_dir
        else:
            makedirs( themes_dir )
            return themes_dir


if __name__ == '__main__':
    set_rcfile()
    set_themes_dir()
