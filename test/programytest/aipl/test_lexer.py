from programy.aipl.lexer import Lexer
from programy.aipl.reader import TextLineReader


class TestLexer:

    def test_movement(self):
        code = """
        ( category (
            ( topic (*) )
            ( that  (*) )
            ( pattern (HELLO WORLD) )
            ( template (Hi there) )
        )
        """

        lexer = Lexer(TextLineReader(code))

        assert lexer
        assert lexer.has_next()
        assert lexer.current() == (2, 1, '(')
        assert lexer.next() == (2, 2, 'category')
        assert lexer.current() == (2, 2, 'category')
        assert lexer.next() == (2, 3, '(')
        lexer.put_back()
        assert lexer.next() == (2, 3, '(')
        lexer.put_back()
        lexer.put_back()
        assert lexer.next() == (2, 2, 'category')

        lexer.reset()
        assert lexer.has_next() is True
        assert lexer.current()[2] == '('
        assert lexer.next()[2] ==  'category'
        assert lexer.next()[2] == '('
        assert lexer.next()[2] == '('
        assert lexer.next()[2] == 'topic'
        assert lexer.next()[2] == '('
        assert lexer.next()[2] == '*'
        assert lexer.next()[2] == ')'
        assert lexer.next()[2] == ')'
        assert lexer.next()[2] == '('
        assert lexer.next()[2] == 'that'
        assert lexer.next()[2] == '('
        assert lexer.next()[2] == '*'
        assert lexer.next()[2] == ')'
        assert lexer.next()[2] == ')'
        assert lexer.next()[2] == '('
        assert lexer.next()[2] == 'pattern'
        assert lexer.next()[2] == '('
        assert lexer.next()[2] == 'HELLO'
        assert lexer.next()[2] == 'WORLD'
        assert lexer.next()[2] == ')'
        assert lexer.next()[2] == ')'
        assert lexer.next()[2] == '('
        assert lexer.next()[2] == 'template'
        assert lexer.next()[2] == '('
        assert lexer.next()[2] == 'Hi'
        assert lexer.next()[2] == 'there'
        assert lexer.next()[2] == ')'
        assert lexer.next()[2] == ')'
        assert lexer.next()[2] == ')'
        assert lexer.has_next() is False

    def test_lex_from_text(self):

        code = """
        ( category (
            ( topic (*) )
            ( that  (*) )
            ( pattern (HELLO WORLD) )
            ( template (Hi there) )
        )
        """

        lexer = Lexer(TextLineReader(code))

        assert lexer
        assert lexer.lexes
        assert lexer.length == 30

        assert lexer.lexes[0] == (2, 1, '(')
        assert lexer.lexes[1] == (2, 2, 'category')
        assert lexer.lexes[2] == (2, 3, '(')

        assert lexer.lexes[3] == (3, 1, '(')
        assert lexer.lexes[4] == (3, 2, 'topic')
        assert lexer.lexes[5] == (3, 3, '(')
        assert lexer.lexes[6] == (3, 4, '*')
        assert lexer.lexes[7] == (3, 5, ')')
        assert lexer.lexes[8] == (3, 6, ')')
