# termcolors #

A simple script to quickly switch between color themes in urxvt.

By keeping persistent settings in .Xresources (font, perl-extenstions, behavior, etc) separate from color settings saved by theme name, this automates changing and applying different color settings.

## Setup ##
1. Requires 'xrdb'
2. Theme files are .Xresources format, should be located in ~/.config/termcolors/themes and have no file extensions. Have a look in themes/ for some examples.
3. Remove all color settings from ~/.Xresources if present
4. (optionally) add to path
**ignore settings.py and getdots.py for now**


Included are some themes I like from http://dotshare.it

```
$ mkdir -p ~/.config/termcolors/themes
$ cp -r themes/ ~/.config/termcolors/
```

## Usage ##
Personally, I make the script executeable and keep in /usr/local/bin/
```
$ chmod +x termcolors.py
$ sudo cp termcolors.py /usr/local/bin/termcolors
```

Then call from anywhere:
```
$ termcolors
```

```
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
```

### TODO: ###
    - select theme directory
    - auto format themefiles
    - adjust transparency setting in themefiles
    - PyPI
    - LICENSE
    
