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
    try:
        # matched = match.groupdict()
        matched = match.group()
        other = match[0]
        another = match[1]
        spanned = match.span()
    except AttributeError:
        matched = ''
        # Or raise an exception
    finally:
        string = my_dict.get(matched, '')
    return string


def main():
    name1 = 'L & S Lighting Corp'
    name2 = 'S. & P. Tax Solutions '
    name3 = 'I.B. Quality Cabinets'
    name4 = 'CH& CP Kitchen Cabinet Gallery'
    name5 = 'D.O.M.'
    pattern = re.compile(r'[&-/+\']')
    repl = pattern.sub(replace_match, name4, count=1)
    rep = re.sub(r'[&-/+\']', '', name4)
    # first = first_word(name2)
    return


if __name__ == '__main__':
    main()
    print('main - done')