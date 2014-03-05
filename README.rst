*********
dotcolors
*********

Simplifies managing Xresources colors.

-----
Setup
-----
Put all global settings in ~/.Xresources (fonts, scrollbars, etc). The idea here is too separate global settings from color settings. My ~/.Xresources looks like this:

::
    urxvt.font:xft:Menlo for Powerline:regular:size=12:antialias=true:hinting=true
    urxvt.scrollBar: false
    urxvt.cursorBlink:1
    urxvt.iconFile: /usr/share/icons/custom/terminal_icon.png
    urxvt.perl-ext-common:default,matcher,fullscreen,vtwheel
    urxvt.perl-ext:default,url-select
    urxvt.urlLauncher:firefox
    urxvt.matcher.button:1
    urxvt.keysym.C-Delete:perl:matcher:last
    urxvt.keysym.M-Delete:perl:matcher:list
    urxvt.keysym.M-u:perl:url-select:select_next
    urxvt.keysym.F11:perl:fullscreen:switch
    urxvt.underlineURLs:true
    urxvt.tabbed.tabbar-fg: 2
    urxvt.tabbed.tabbar-bg: 0
    urxvt.tabbed.tab-fg:3
    urxvt.tabbed.tab-bg:0
    urxvt.loginShell:true

    xpdf.viKeys: true
    xpdf.initialZoom: width


So now dotcolors will first load settings from whichever theme file is selected, then merge global settings from ~/.Xresources.

-----
Usage
-----
::

   Usage: dotcolors

   dotcolors [-h]
   dotcolors [-s] [(-r <per_page>)] [-t]
   dotcolors [(-s <limit>)] [(-r <per_page>)] [-t]
   dotcolors [--setup]

   -h --help     Display this screen

   -s --sync     Download themes, optionally limit the
                  number of themes downloaded with <limit>,
                  default=all

   --setup       create default directorie and config

   -r --results  Number of results to display per page

   -t --test     Apply changes without writing to file

=====
TODO
=====
* show number of themes found/downloading: "Fetching theme (21/100)"
* auto format themefiles
* adjust transparency setting in themefiles
