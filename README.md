# termcolors #

A simple script to quickly switch between color themes in urxvt.

## Setup ##
1. Requires 'xrdb'
2. Theme files are .Xresources format, should be located in ~/.config/xresources/ and have no file extensions.
3. Remove all color settings from ~/.Xresources
4. (optionally) add to path

Included are some themes I like from http://dotshare.it


$mkdir -p ~/.config/xresources
$cp xresources/* ~/.config/xresources/

## Usage ##
Personally, I make the script executeable and keep in /usr/local/bin:

$chmod + termcolors.py
$sudo cp termcolors.py /usr/local/bin/termcolors

Then call from anywhere:
$termcolors

  =========================
   1) autumn
   2) baskerville
   3) bleh
   4) crshd
   5) erosion
   6) fishbone
   7) house
   8) insignificato
   9) julie
  10) mnml
  11) navy
  12) nudge
  13) oblivion
  14) papyrus-dark
  15) parkerbros
  16) sexcolors
  17) twilight
  =========================
  Current theme is: mnml
  
  Enter number of selection: 


### TODO: ###
    - browse and preview themes from dotshare.it
    - download and auto format themefiles
    - adjust transparency setting in themefiles