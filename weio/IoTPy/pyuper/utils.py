import sys, os


class IoTPy_APIError(Exception):
    pass

class IoTPy_IOError(Exception):
    pass

class IoTPy_ThingError(Exception):
    pass

def errmsg(fmt, *args):
    if not fmt.endswith('\n'):
        fmt += '\n'
    sys.stderr.write(os.path.basename(sys.argv[0]))
    sys.stderr.write(': ')
    if len(args):
        sys.stderr.write(fmt % args)
    else:
        sys.stderr.write(fmt)
    sys.stderr.flush()


def die(fmt, *args):
    if not fmt.endswith('\n'):
        fmt += '\n'
    sys.stderr.write(os.path.basename(sys.argv[0]))
    sys.stderr.write(': ')
    if len(args):
        sys.stderr.write(fmt % args)
    else:
        sys.stderr.write(fmt)
    sys.stderr.flush()
    sys.exit(1)


