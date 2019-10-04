import pytest
from programy.aipl.tokenizer import Tokenizer
from programy.aipl.tokenizer import TokenizerException
from programy.aipl.lexer import Lexer
from programy.aipl.reader import TextLineReader


class TestLexer(Lexer):

    def __init__(self, testlexes):
        Lexer.__init__(self)
        self._lexes = testlexes[:]
        self._len = len(self._lexes)

    def _lex(self):
        pass


class TestTokenizerException:

    def test_show_aipl_error_for_token(self):
        tokenizer = Tokenizer(Lexer(TextLineReader("""
        ( category (
                ( topic (*) )
                ( that (*) )
                ( pattern (HELLO *) )
                ( template (Hi there!) )
            )
        )
        """)))

        code = TokenizerException.get_aipl_error_for_token(tokenizer.lexer.linereader, (2, 2, 'topic'))
        assert len(code) == 4
        assert code[0] == "1:         ( category ("
        assert code[1] == "2:                 ( topic (*) )"
        assert code[2] == "                     ^-----"
        assert code[3] == "3:                 ( that (*) )"



class TestTokenizer:

    def test_tokenizer_methods(self):

        tokenizer = Tokenizer(Lexer(TextLineReader("""
        ( category (
                ( topic (*) )
                ( that (*) )
                ( pattern (HELLO *) )
                ( template (Hi there!) )
            )
        )
        """)))

        assert tokenizer
        assert tokenizer.tokens
        assert not tokenizer.errors
        assert tokenizer.length == 1

        assert tokenizer.current() == ([(3, 4, '*')], [(4, 4, '*')], [(5, 4, 'HELLO'), (5, 5, '*')], [(6, 4, 'Hi'), (6, 5, 'there!')])
        assert tokenizer.has_next() is False

    def test_check_for_bracket(self):
        tokenizer = Tokenizer(TestLexer([(1, 1, '{'), [2, 1, ')']]))

        with pytest.raises(TokenizerException):
            tokenizer._check_for_bracket('(')

    def test_parse_template_inner_clause(self):
        tokenizer = Tokenizer(TestLexer([(1, 1, '('), [2, 1, '*'], [3, 1, ')']]))

        tokenizer._parse_template_inner_clause()

    def test_parse_template_inner_clause_no_close(self):
        tokenizer = Tokenizer(TestLexer([(1, 1, '('), [2, 1, '*'], [3, 1, '*']]))

        with pytest.raises(TokenizerException):
            tokenizer._parse_template_inner_clause()
