class TokenInfo:
    def __init__(self, regex_line, modifiers):
        self.regex_line = regex_line
        self.modifiers = tuple(modifiers)

    def __eq__(self, other):
        if isinstance(other, TokenInfo):
            return (
                self.regex_line == other.regex_line and
                self.modifiers == other.modifiers)
        return False

    def __str__(self):
        return ("regex_line:{}, modifiers:{}"
                .format(self.regex_line, self.modifiers))
