import re
from programy.aipl.lexer import Lexer


class TokenizerException(Exception):

    def __init__(self, msg, token=None):
        Exception.__init__(self)
        self._msg = msg
        self._token = token

    def __str__(self):
        if self._token:
            return "{0} - {1}".format(self._msg, TokenizerException.token_to_string(self._token))
        else:
            return self._msg

    @staticmethod
    def token_to_string(token):
        return "Line:{0}, Position:{1}, Token:'{2}'".format(token[0], token[1], token[2])

    @staticmethod
    def get_aipl_error_for_token(reader, token):
        result = []

        if token[0] > 1:
            result.append("{0}: {1}".format(token[0]-1, reader.lines[token[0]-1][1]))

        result.append("{0}: {1}".format(token[0], reader.lines[token[0]][1]))

        result.append(TokenizerException.get_highlighted_error_token(reader.lines[token[0]][1], token))

        if token[0] > 0:
            if token[0]-1 < reader.length:
                result.append("{0}: {1}".format(token[0]+1, reader.lines[token[0]+1][1]))

        return result

    @staticmethod
    def get_highlighted_error_token(line, token):
        position = token[1]
        splits = re.split("(\s+)", line)
        count = 1
        length = 0
        for split in splits:
            splitlen = len(split)
            split = split.strip()
            if split:
                if count == position:
                    arrow = ""
                    if length > 0:
                        arrow = ' ' * (length-1)
                    underline = '-' * splitlen
                    return "    {0}^{1}".format(arrow, underline)
                count += 1
            length += splitlen


class Tokenizer:

    CATEGORY = 'category'
    TOPIC = "topic"
    THAT = "that"
    PATTERN = "pattern"
    TEMPLATE = "template"

    LINE = 0
    POSITION = 1
    TOKEN = 2

    def __init__(self, lexer: Lexer):
        self._lexer = lexer
        self._num = 0
        self._tokens = []
        self._errors = []
        self._tokenize()
        self._len = len(self._tokens)

    @property
    def lexer(self):
        return self._lexer

    @property
    def tokens(self):
        return list(self._tokens)

    @property
    def length(self):
        return self._len

    @property
    def errors(self):
        return list(self._errors)

    def __iter__(self):
        self._num = 0
        return self

    def __next__(self):
        return self.next()

    def reset(self):
        self._num = 0

    def current(self):
        return self._tokens[self._num]

    def has_next(self):
        return bool(self._num == self._len)

    def view_next(self):
        return self._tokens[self._num + 1]

    def next(self):
        if self._num >= self._len:
            raise StopIteration()
        self._num += 1
        return self._tokens[self._num]


    def _tokenize(self):
        try:
            while self._lexer.has_next():
                self._parse_clause()
                if self._lexer.has_next():
                    token = self._lexer.next()

        except StopIteration:
            self._errors.append("Syntax error, incomplete grammar")

        except TokenizerException as toke:
            self._errors.append(str(toke))

    def _parse_clause(self, topic=None):
        self._check_for_bracket(Lexer.OPENBRACKET)

        token = self._lexer.next()
        if token[Tokenizer.TOKEN] == Tokenizer.TOPIC:
            self._parse_topic_categories()

        elif token[Tokenizer.TOKEN] == Tokenizer.CATEGORY:
            self._parse_category(topic=topic)

        else:
            raise TokenizerException("Missing 'category'", token)

        self._check_for_bracket(Lexer.CLOSEBRACKET)

        if self._lexer.has_next():
            token = self._lexer.next()

    def _parse_topic_categories(self):

        token = self._lexer.next()
        topic = self._parse_pattern_match_clause()

        token = self._lexer.next()
        self._check_for_bracket(Lexer.OPENBRACKET)
        while token[Tokenizer.TOKEN] != Lexer.CLOSEBRACKET:

            token = self._lexer.next()
            if token[Tokenizer.TOKEN] == Tokenizer.CATEGORY:
                self._parse_category(topic=topic)

            token = self._lexer.next()
            self._check_for_bracket(Lexer.CLOSEBRACKET)

            if self._lexer.has_next():
                token = self._lexer.next()

    def _parse_category(self, topic=None):
        token = self._lexer.next ()
        self._check_for_bracket(Lexer.OPENBRACKET)

        topic = topic
        that = None
        pattern = None
        template = None

        token = self._lexer.next()
        while token[Tokenizer.TOKEN] != Lexer.CLOSEBRACKET:

            self._check_for_bracket(Lexer.OPENBRACKET)
            token = self._lexer.next()

            if token[Tokenizer.TOKEN] == Tokenizer.TOPIC:
                topic = self._parse_topic_clause()

            elif token[Tokenizer.TOKEN] == Tokenizer.THAT:
                that = self._parse_that_clause()

            elif token[Tokenizer.TOKEN] == Tokenizer.PATTERN:
                pattern = self._parse_pattern_clause()

            elif token[Tokenizer.TOKEN] == Tokenizer.TEMPLATE:
                template = self._parse_template_clause()

            token = self._lexer.next()
            self._check_for_bracket(Lexer.CLOSEBRACKET)

            token = self._lexer.next()

        if topic is None:
            topic = [(-1, -1, '*')]

        if that is None:
            that = [(-1, -1, '*')]

        self._tokens.append((topic, that, pattern, template))

    def _parse_topic_clause(self):
        token = self._lexer.next ()
        self._check_for_bracket(Lexer.OPENBRACKET)

        pattern = self._parse_pattern_match_clause()

        self._check_for_bracket(Lexer.CLOSEBRACKET)

        return pattern

    def _parse_that_clause(self):
        token = self._lexer.next ()
        self._check_for_bracket(Lexer.OPENBRACKET)

        pattern = self._parse_pattern_match_clause()

        self._check_for_bracket(Lexer.CLOSEBRACKET)

        return pattern

    def _parse_pattern_clause(self):
        token = self._lexer.next ()
        self._check_for_bracket(Lexer.OPENBRACKET)

        pattern = self._parse_pattern_match_clause()

        self._check_for_bracket(Lexer.CLOSEBRACKET)

        return pattern

    def _parse_pattern_match_clause(self):
        pattern = []
        token = self._lexer.next()
        while token[Tokenizer.TOKEN] != Lexer.CLOSEBRACKET:
            pattern.append(token)
            token = self._lexer.next()

        return pattern

    def _parse_template_clause(self):
        token = self._lexer.next ()
        self._check_for_bracket(Lexer.OPENBRACKET)

        template = self._parse_template_inner_clause()

        self._check_for_bracket(Lexer.CLOSEBRACKET)

        return template

    def _parse_template_inner_clause(self):
        template = []
        token = self._lexer.next()
        while token[Tokenizer.TOKEN] != Lexer.CLOSEBRACKET:
            template.append(token)
            if self._lexer.has_next():
                token = self._lexer.next()

            else:
                raise TokenizerException("Syntax error")

        return template

    def _check_for_bracket(self, bracket):
        token = self._lexer.current()
        if token[Tokenizer.TOKEN] == bracket:
            return

        raise TokenizerException("Missing {0}".format(bracket))

