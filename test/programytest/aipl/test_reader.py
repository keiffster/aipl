from programy.aipl.reader import TextLineReader
from programy.aipl.reader import FileLineReader


class TestFileReader:

    def test_readfile(self):

        file_reader = FileLineReader('./test.aipl')

        assert file_reader
        assert file_reader.lines
        assert file_reader.length == 5
        assert (1, "") == file_reader.lines[0]
        assert (2, "line1") == file_reader.lines[1]
        assert (3, "line2") == file_reader.lines[2]
        assert (4, "line3") == file_reader.lines[3]
        assert (5, "") == file_reader.lines[4]


class TestLineReader:

    def test_readlines(self):

        text_reader = TextLineReader("""
        line1
        line2
        line3
        """)

        assert text_reader
        assert text_reader.lines
        assert text_reader.length == 5
        assert (1, "") == text_reader.lines[0]
        assert (2, "line1") == text_reader.lines[1]
        assert (3, "line2") == text_reader.lines[2]
        assert (4, "line3") == text_reader.lines[3]
        assert (5, "") == text_reader.lines[4]
