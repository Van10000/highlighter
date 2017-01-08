import functools
import itertools
import re
import operator

from TokenInfo import TokenInfo
from Constants import *


class LanguageFormat:
    MODIFIERS_DICT = {case_insensitive: re.IGNORECASE, dotall: re.DOTALL}

    def __init__(self, tokens_info, general_modifiers):
        self.tokens_info = tokens_info
        self.modifiers = general_modifiers

    def get_reg_exs(self):
        for token_info in self.tokens_info:
            modifiers = list(itertools.chain(self.modifiers,
                                             token_info.modifiers))
            modifiers_combined = LanguageFormat._combine_modifiers(*modifiers)
            yield re.compile(token_info.regex_line, modifiers_combined)

    @staticmethod
    def create_from_lines(lines):
        general_modifiers = list(LanguageFormat.get_modifiers(lines[0]))
        tokens_info = list(LanguageFormat.get_tokens_info(lines[1:]))
        return LanguageFormat(tokens_info, general_modifiers)

    @staticmethod
    def get_tokens_info(lines):
        for line in lines:
            for i in range(len(line)):
                if line[i] in "(^":
                    cur_regex = line[i:]
                    cur_modifiers = LanguageFormat.get_modifiers(line[:i])
                    break
            yield TokenInfo(cur_regex, cur_modifiers)
        yield TokenInfo("(?P<line_break>\n)", [])

    @staticmethod
    def get_modifiers(line):
        modifiers_strings = filter(None, line.split(' '))
        return LanguageFormat._get_modifiers_ints(modifiers_strings)

    @staticmethod
    def _get_modifiers_ints(modifiers_strings):
        return [LanguageFormat._get_modifier_int(string)
                for string in modifiers_strings]

    @staticmethod
    def _get_modifier_int(modifier_string):
        try:
            return LanguageFormat.MODIFIERS_DICT[modifier_string]
        except KeyError:
            raise Exception("Unknown modifier:{}".format(modifier_string))

    @staticmethod
    def _combine_modifiers(*modifiers):
        return functools.reduce(operator.or_, modifiers, 0)
