from collections import OrderedDict

from ParsedToken import ParsedToken
from Constants import *


def tokenize(code, reg_exs):
    occurrences = OrderedDict()
    for regex in reg_exs:
        occurrence = regex.search(code)
        if occurrence is not None:
            occurrences[regex] = occurrence
            groups = occurrence.groupdict()
            if len(groups) != 1:
                raise Exception("There should be exactly one named group "
                                "for each regular expression.\n"
                                "Given regular expression {} has "
                                "following named groups:{}"
                                .format(regex.re.pattern, groups))
    pos = 0
    while True:
        for regex, occurrence in occurrences.items():
            if occurrence is not None and \
               occurrence.start(occurrence.lastgroup) < pos:
                new_occurrence = regex.search(code, pos)
                occurrences[regex] = new_occurrence

        cur_group = min(filter(None, occurrences.values()),
                        key=lambda occ: occ.start(occ.lastgroup),
                        default=None)
        if cur_group is None:
            if pos < len(code):
                yield ParsedToken(simple_code, pos, code[pos:])
            break
        start = cur_group.start(cur_group.lastgroup)
        end = cur_group.end(cur_group.lastgroup)
        if pos != cur_group.start(cur_group.lastgroup):
            yield ParsedToken(simple_code, pos, code[pos:start])
        yield ParsedToken(cur_group.lastgroup, start, code[start:end])
        pos = end


def _reset_if_not_none(dictionary, key, value):
    if value is None:
        del dictionary[key]
    else:
        dictionary[key] = value
