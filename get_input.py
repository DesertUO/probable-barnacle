# Input check
def getchar():
    ch = ''
    # Returns a single character from standard input
    # Windows version
    # import msvcrt
    # ch = msvcrt.getch()
    # Linux version
    import tty
    import termios
    import sys

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch
