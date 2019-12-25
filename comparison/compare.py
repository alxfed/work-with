from . import constants
import re
import nltk
from nltk.tokenize import RegexpTokenizer


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


def first_word(name):
    # 1. length is less than 10
    # 2. length is more than 10
    frst_word = ''
    tokenizer = RegexpTokenizer("\w+\.?\s+?[-/\+'&]\s+\w+\.?") # |\w+\s&' \w+&?\s+.\
    tokens = tokenizer.tokenize(name)
    if tokens:
        frst_word = tokens[0]
    return frst_word


def are_the_same(name:str, comparable:str, same:float):
    yes = False
    return yes


def jaccard_dist(a:set, b:set) -> float:
    jd = nltk.jaccard_distance(a, b)
    return jd

'''
    # combinations = ['. ', ' ', '.']
    # sepp = ['&', '-', '/', '+', "'"]
    # name = name.strip(' .')
    # length = len(name)
    # no_spaces = length - len(name.replace(' ', ''))
    # no_periods = length - len(name.replace('.', ''))
    # no_commas = length - len(name.replace(',', ''))
    # no_dashes = length - len(name.replace('-', ''))
    # and_sign = length - len(name.replace('&', ''))
    # if not no_spaces == 0: # there are spaces to work with
    #     one, sep, rest = name.partition(' ') # let's try the first split
    #     if len(one) - len() == 0: # probably some abbreviation, maybe with dots
    #         pass
    # else: # no_spaces == 0
    #     if not no_periods == 0: # no spaces but some periods. A domain name?
    #         one, sep, rest = name.partition('.')
    #     else: # no spaces and no periods
    #         if not no_dashes == 0:
    #             one, sep, rest = name.partition('-')
    # repl = name.replace('. ', '', 1)
    # if len(one) < 3:
    #

'''