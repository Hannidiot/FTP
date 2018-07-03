__all__ = ['standardize_list', 'parse']


def standardize_list(a):
    s = ''
    for i in a:
        for k in i:
            s += "{} ".format(str(k))
        s += '\t'
    return s


def parse(string):
    pieces = string.split("\t")[:-1]
    info = [(x for x in piece.split(" ")[:-1]) for piece in pieces]
    return info
