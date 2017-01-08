import unittest
import re
from LanguageFormat import LanguageFormat
from ParsedToken import ParsedToken
from TokenInfo import TokenInfo
import Tokenizing
from Constants import *


class LanguageFormatTests(unittest.TestCase):
    def test_get_tokens_info(self):
        regex = "(?P<regex>regex)"
        lines = [regex]
        expected_token_info = TokenInfo(regex, [])
        tokens_info = list(LanguageFormat.get_tokens_info(lines))
        self.assertEqual(tokens_info[0], expected_token_info)

    def test_get_tokens_info_with_modifiers(self):
        modifiers = "case_insensitive"
        regex = "(?P<regex>regex)"
        lines = ["{} {}".format(modifiers, regex)]
        expected_token_info = TokenInfo(regex, [re.IGNORECASE])
        tokens_info = list(LanguageFormat.get_tokens_info(lines))
        self.assertEqual(tokens_info[0], expected_token_info)

    def test_get_many_tokens_info(self):
        reg_exs = ["(?P<re>abc)(?:def)", "(?P<a>a)"]
        expected_tokens_info = [TokenInfo(reg_exs[0], []),
                                TokenInfo(reg_exs[1], [])]
        tokens_info = list(LanguageFormat.get_tokens_info(reg_exs))
        for token, exp_token in zip(tokens_info,
                                    expected_tokens_info):
            self.assertEqual(token, exp_token)

    def test_create_from_lines(self):
        lines = ["case_insensitive", "(?P<a>a)"]
        lang_format = LanguageFormat.create_from_lines(lines)
        self.assertSetEqual(set(lang_format.modifiers), {re.IGNORECASE})
        self.assertEqual(lines[1], lang_format.tokens_info[0].regex_line)


class TokenizingTests(unittest.TestCase):
    def test_tokenize_simple(self):
        reg_exs = (re.compile("(?P<br>\n)"), re.compile("(?P<abc>abc)"))
        text = "abc\nabc"
        expected_tokens = [ParsedToken("abc", 0, "abc"),
                           ParsedToken("br", 3, '\n'),
                           ParsedToken("abc", 4, "abc")]
        tokens = list(Tokenizing.tokenize(text, reg_exs))
        self.assertListEqual(tokens, expected_tokens)

    def test_tokenize_simple_code(self):
        reg_exs = []
        text = "Hello, world!"
        expected_tokens = [ParsedToken(simple_code, 0, text)]
        tokens = list(Tokenizing.tokenize(text, reg_exs))
        self.assertListEqual(tokens, expected_tokens)

    def test_tokenize_with_simple_code(self):
        reg_exs = [re.compile("(?P<a>a)")]
        text = "aba"
        expected_tokens = [ParsedToken("a", 0, "a"),
                           ParsedToken("simple_code", 1, "b"),
                           ParsedToken("a", 2, "a")]
        tokens = list(Tokenizing.tokenize(text, reg_exs))
        self.assertListEqual(tokens, expected_tokens)

    def test_tokenize_considers_order(self):
        reg_exs = [re.compile("(?P<a>a)"), re.compile("(?P<ab>ab)"),
                   re.compile("(?P<ba>ba)"), re.compile("(?P<b>b)")]
        text = "aba"
        expected_tokens = [ParsedToken("a", 0, "a"),
                           ParsedToken("ba", 1, "ba")]
        tokens = list(Tokenizing.tokenize(text, reg_exs))
        self.assertListEqual(tokens, expected_tokens)

if __name__ == "__main__":
    unittest.main()