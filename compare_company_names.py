# -*- coding: utf-8 -*-
"""...
"""
import re
import comparison


def main():
    name1 = 'D. & Sp. Construction Company'
    name2 = 'S  & P Company Construction'
    for example in comparison.constants.TEST_EXAMPLES:
        first_word_n = comparison.compare.first_word(example)
        trans_word_n = re.sub('[ .-/]', '', first_word_n)
        print(example, '  first word:   ', first_word_n, 'trans word:  ', trans_word_n)
    yes_or_no = comparison.compare.are_the_same(name=name1, comparable=name2, same=0.01)
    return


if __name__ == '__main__':
    main()
    print('main - done')

'''


def main():
    name1 = 'L & S Lighting Corp'
    name2 = 'SoPf. & P. Tax Solutions '
    name7 = 'S . & P Tax Solutions'
    name3 = 'I.B. Quality. Cabinets'
    name4 = 'CH& CP Kitchen Cabinet Gallery'
    name5 = 'D.O.M.'
    nname = 'one two'
    c = constants.LIST_OF_JOINERS
    a = set(name2)
    b = set(name7)
    jd = jaccard_dist(a, b)
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
'''