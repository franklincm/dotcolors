#!/usr/bin/env python2

from docopt import docopt
import sys
import core
import settings
import getdots

def main():
    usage = """
    
    Usage: 
    termcolors [-h]
    termcolors [-s] [(-r <per_page>)] [-t]
    termcolors [(-s <limit>)] [(-r <per_page>)] [-t]
    termcolors [--setup]
    
    -h --help     Display this screen
    
    -s --sync     Download themes, optionally limit the
                  number of themes downloaded with <limit>,
                  default=all

    --setup       create default directorie and config
    
    -r --results  Number of results to display per page
    
    -t --test     Apply changes without writing to file
    
    """ 
    
    options = docopt(usage)
    #print options
    
    
    # options = {'--help': False,
    #            '--results': False,
    #            '--setup': False,
    #            '--sync': False,
    #            '--test': False,
    #            '<limit>': None,
    #            '<results>': None}
    
    
    if(options['--setup']):
        settings.set_rcfile()
        settings.gset_themes_dir()

        
    if(options['--sync']):
        limit = int(options['<limit>'])
        if type(limit) == type(None):
            limit = 200
        getdots.run(limit)


    if(options['--results']):
        results = int(options['<per_page>'])
        

    try:
        colors = core.get_colors()
        current = core.get_current()

        selection = core.getch_selection(colors, results)
        print selection
        core.write_changes(current, selection, 
                                 options['--test'])

    except KeyboardInterrupt:
        sys.exit(0)
            
            
if __name__ == '__main__':
    main()
