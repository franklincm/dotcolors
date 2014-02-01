# termcolors #

Simplifies managing Xresources colors.

## Usage ##
```
    Usage: ./termcolors
    
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
```

### TODO: ###
    - show number of themes found/downloading: "Fetching theme (21/100)"
    - auto format themefiles
    - adjust transparency setting in themefiles
    - PyPI
