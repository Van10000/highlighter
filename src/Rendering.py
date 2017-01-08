from dominate import document
from dominate.tags import br, span, style
from Constants import *


def build_html(parsed_tokens, css_style):
    with document(title="Code") as doc:
        style(css_style)
        for token in parsed_tokens:
            if token.type == line_break:
                br()
            else:
                lines = token.content.split('\n')
                for j in range(len(lines)):
                    if j != 0:
                        br()
                    span(lines[j], cls=token.type)
    return doc.render(pretty=False)
