import collections


class ParsedToken():
    def __init__(self, token_type, start_pos, content):
        self.type = token_type
        self.start_pos = start_pos
        self.content = content

    def __eq__(self, other):
        if isinstance(other, ParsedToken):
            return (self.type == other.type and
                    self.start_pos == other.start_pos and
                    self.content == other.content)
        return False
