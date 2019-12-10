import re
# from .constants import *


def first_word(name):
    name = name.strip(' .')
    length = len(name)
    no_spaces = length - len(name.replace(' ', ''))
    repl = name.replace('. ', '', 1)
    no_periods = length - len(name.replace('.', ''))
    no_commas = length - len(name.replace(',', ''))
    no_dashes = length - len(name.replace('-', ''))
    and_sign = length - len(name.replace('&', ''))
    one, sep, rest = name.partition(' ')
    # if len(one) < 3:
    #
    return first_word


def main():
    name1 = 'L & S Lighting Corp'
    name2 = 'S. & P. Tax Solutions '
    name3 = 'I.B. Quality Cabinets'
    name4 = 'C&H Kitchen Cabinet Gallery'
    name5 = 'D.O.M.'
    first = first_word(name2)
    return


if __name__ == '__main__':
    main()
    print('main - done')