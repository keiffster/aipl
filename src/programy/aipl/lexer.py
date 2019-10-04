from programy.aipl.reader import LineReader


class Lexer:

    OPENBRACKET = '('
    SPACEDOPENBRACKET = ' {0} '.format(OPENBRACKET)
    CLOSEBRACKET = ')'
    SPACEDCLOSEBRACKET = ' {0} '.format(CLOSEBRACKET)

    def __init__(self, linereader: LineReader = None):
        self._linereader = linereader
        self._lexes = []
        self._num = 0
        self._lex()
        self._len = len(self._lexes)

    @property
    def linereader(self):
        return self._linereader

    @property
    def lexes(self):
        return list(self._lexes)

    @property
    def length(self):
        return self._len

    def _lex(self):
        self._lexes.clear()
        for line in self._linereader:
            text = line[1].strip()
            if text and not text.startswith('#'):
                self._lexes.extend([(line[0], x, y) for x, y in enumerate(self._parse_into_lexes(text), 1)])

    def _parse_into_lexes(self, line: str) -> []:
        return line.replace(Lexer.OPENBRACKET, Lexer.SPACEDOPENBRACKET). \
            replace(Lexer.CLOSEBRACKET, Lexer.SPACEDCLOSEBRACKET). \
            split()

    def reset(self):
        self._num = 0

    def current(self):
        return self._lexes[self._num]

    def has_next(self):
        return bool(self._num+1 < self._len)

    def view_next(self):
        return self._lexes[self._num + 1]

    def next(self):
        if self._num >= self._len:
            raise StopIteration()
        self._num += 1
        return self._lexes[self._num]

    def put_back(self):
        if self._num > 0:
            self._num -= 1

