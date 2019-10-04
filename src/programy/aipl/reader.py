

class LineReader:

    def __init__(self):
        self._lines = []
        self._num = 0
        self._len = len(self._lines)

    @property
    def lines(self):
        return list(self._lines)

    @property
    def length(self):
        return self._len

    def __iter__(self):
        self._num = 0
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self._num >= self._len:
            raise StopIteration()
        num = self._num
        self._num += 1
        return self._lines[num]


class FileLineReader(LineReader):

    def __init__(self, filename):
        LineReader.__init__(self)
        self._read_lines_from_file(filename)

    def _read_lines_from_file(self, filename):
        with open(filename, "r+") as language:
            num = 1
            for aline in language:
                self._lines.append((num, aline))
                num += 1
        self._len = len(self._lines)


class TextLineReader(LineReader):

    def __init__(self, text):
        LineReader.__init__(self)
        self._lines = [(count, line) for count, line in enumerate(text.split("\n"), 1)]
        self._len = len(self._lines)

