import re
# from .constants import *


def first_word(name):
    combinations = ['. ', ' ', '.']
    sepp = ['&', '-', '/', '+', "'"]
    name = name.strip(' .')
    length = len(name)
    no_spaces = length - len(name.replace(' ', ''))
    no_periods = length - len(name.replace('.', ''))
    no_commas = length - len(name.replace(',', ''))
    no_dashes = length - len(name.replace('-', ''))
    and_sign = length - len(name.replace('&', ''))
    if not no_spaces == 0: # there are spaces to work with
        one, sep, rest = name.partition(' ') # let's try the first split
        if len(one) - len() == 0: # probably some abbreviation, maybe with dots
            pass
    else: # no_spaces == 0
        if not no_periods == 0: # no spaces but some periods. A domain name?
            one, sep, rest = name.partition('.')
        else: # no spaces and no periods
            if not no_dashes == 0:
                one, sep, rest = name.partition('-')
    repl = name.replace('. ', '', 1)
    # if len(one) < 3:
    #
    return first_word


def replace_match(match):
    # https://docs.python.org/2.0/lib/match-objects.html
    # https://docs.python.org/3/library/re.html#match-objects
    my_dict = {'&': 'and'}
    string = ''
    if match:
        # matched = match.groupdict()
        matched = match.group()
        st = match.start()
        en = match.end()
        spa = match.span()
        other = match[0]
        spanned = match.span()
    else:
        string = ''
    return string


def main():
    name1 = 'L & S Lighting Corp'
    name2 = 'SoPf. & P. Tax Solutions '
    name3 = 'I.B. Quality. Cabinets'
    name4 = 'CH& CP Kitchen Cabinet Gallery'
    name5 = 'D.O.M.'
    nname = 'one two'
    pattern = re.compile(r'[&-/+\']')
    # body = re.sub('>\s*<', '><', body, 0, re.M)
    mate = re.match(r'(?:[.\w+])+', name2)
    ma = mate.groups()
    # ["](?P<protocol>http(?P<secure>s)?://)(?P<fqdn>[a-zA-Z0-9]*(?P<subdomain>(.)[a-zA-Z0-9]*)*)[/](?P<filename>([a-zA-Z.])*)["]
    m = re.match(r'(?P<first>\w+) (?P<middle>\w+) (?P<last>\w+)', 'jane m doe')
    di = m.groupdict()
    ma = re.match(r"(?P<first>\w+) (?P<last>\w+)", nname)
    m = ma.groupdict()
    words = re.compile(r'(?P<first>\w+) (?P<second>\b\w+\b)')
    mat = words.match(name2)
    ma = mat.groupdict()
    repl = pattern.sub(replace_match, name4, count=1)
    rep = re.sub(r'[&-/+\']', '', name4)
    # first = first_word(name2)
    return


if __name__ == '__main__':
    main()
    print('main - done')