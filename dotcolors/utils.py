#
# copied from http://code.activestate.com/recipes/134892/
#

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def raw_input_with_default(prompt, default):
    import readline
    def pre_input_hook():
        readline.insert_text(default)
        readline.redisplay()

    readline.set_pre_input_hook(pre_input_hook)
    try:
        return raw_input(prompt)
    finally:
        readline.set_pre_input_hook(None)


def rgb_to_hex(rgba):
    """
    expects: rgba value, ex: 0000/0000/0000/dddd
    returns: hex value, ex: #000000
    ignores alpha value
    """
    rgba = rgba.split('/')
    hex_value = '#' + rgba[0][:2] + rgba[1][:2] + rgba[2][:2]
    return hex_value


def hex_to_rgb(hex_value):
    """
    expects: hex value, ex: #ffffff
    returns: rgb value, ex: ff00/ff00/ff00
    """
    if '#' in hex_value:
        hex_value = hex_value.replace('#', '')
    if len(hex_value) < 6:
        return '0000/0000/0000'
    r = hex_value[:2]
    g = hex_value[2:4]
    b = hex_value[4:]
    return r + '00/' + g + '00/' + b + '00'


def decimal_to_alpha(dec):
    """
    expects: decimal between 0 and 100
    returns: alpha value for rgba
    """
    dec /= 100.0
    alpha =  hex(int(dec*65535))[2:]
    while len(alpha) < 4:
        alpha = '0' + alpha
    return alpha


if __name__ == '__main__':
    print rgb_to_hex('af00/1e00/2d00/aaaa')
    print hex_to_rgb('#af1e2d')
