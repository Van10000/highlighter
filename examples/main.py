from argparse import ArgumentParser
import os

from LanguageFormat import *
from Rendering import build_html
from Tokenizing import tokenize


FORMATS = dict()
STYLES = dict()


def get_cached(lang, cache, ext):
    if lang not in cache:
        path = os.path.join("..", "{}.{}".format(lang, ext))
        with open(path) as lang_file:
            value = lang_file.read().split('\n')
            cache[lang] = value
            return value
    else:
        return cache[lang]


def get_format_rules(lang):
    try:
        return get_cached(lang, FORMATS, "hig")
    except Exception:
        raise Exception("Could not load format file for "
                        "extension {}".format(lang))


def get_css_style(lang):
    try:
        return get_cached(lang, STYLES, "css")
    except Exception:
        raise Exception("Could not load style file for "
                        "extension {}".format(lang))


def get_html_name(name):
    name, ext = os.path.splitext(name)
    return "{}.html".format(name)


def render_to_html(code, rules, style):
    language_format = LanguageFormat.create_from_lines(rules)
    reg_exs = language_format.get_reg_exs()
    tokens = tokenize(code, reg_exs)
    return build_html(tokens, style)


def render_file(input_file, output_dir, output_name, quiet, lang=None):
    try:
        name, ext = os.path.splitext(input_file)
        if lang is None:
            lang = ext[1:]
        rules = get_format_rules(lang)
        style = get_css_style(lang)
        with open(input_file) as code_file:
                code = code_file.read()
        rendered_html = render_to_html(code, rules, style)
        if output_dir and not os.path.exists(output_dir):
            os.mkdir(output_dir)
        with open(os.path.join(output_dir, output_name), "w+") as out_file:
            out_file.write(rendered_html)
    except Exception as e:
        if not quiet:
            print("Could not render file {}".format(input_file))
            print(e)
            print()


def render_directory(input_dir, output_dir, lang, current_dir,
                     file_names, quiet=False):
    relative_path = os.path.relpath(current_dir, input_dir)
    for file_name in file_names:
        input_file = os.path.join(current_dir, file_name)
        output_path = output_dir if relative_path == '.' \
            else os.path.join(output_dir, relative_path)
        render_file(input_file, output_path,
                    get_html_name(file_name), quiet, lang)


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-l", "--lang", default=None,
                            help="Language of code.\n"
                                 "Parsing rules file "
                                 "should be at <lang>.hig.\n"
                                 "Css style file should be at <lang>.css.\n"
                                 "If not specified - language will be defined "
                                 "by code file extension.")
    arg_parser.add_argument("-i", "--input_location", required=True,
                            help="File or directory with code to highlight.")
    arg_parser.add_argument("-o", "--output_location", default=None,
                            help="File or directory for html files.\n"
                                 "If not specified file - result will be at "
                                 "the same directory at file with the "
                                 "same name and extension html.\n"
                                 "If not specified directory - result "
                                 "directory will be at near input "
                                 "directory with name 'result'")
    arg_parser.add_argument("-q", "--quiet", action='store_true',
                            help="If this flag is not set - about every file "
                                 "that program failed to parse it will "
                                 "report in standard output.\n")
    args = arg_parser.parse_args()
    args.input_location = os.path.abspath(args.input_location)
    in_dir, in_file = os.path.split(args.input_location)

    if os.path.isfile(args.input_location):
        if args.output_location is not None:
            out_dir, out_file = os.path.split(args.output_location)
        else:
            out_dir, out_file = in_dir, get_html_name(in_file)
        render_file(args.input_location, out_dir,
                    out_file, args.quiet, args.lang)
    else:
        if args.output_location is None:
            args.output_location = \
                os.path.join(in_dir, "{}_result".format(in_file))
        if not os.path.exists(args.output_location):
            os.mkdir(args.output_location)
        for cur_dir, ignore, file_names in os.walk(args.input_location):
            render_directory(args.input_location, args.output_location,
                             args.lang, cur_dir, file_names, args.quiet)

if __name__ == "__main__":
    main()
