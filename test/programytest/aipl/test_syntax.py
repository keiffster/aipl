from programy.aipl.tokenizer import Tokenizer
from programy.aipl.lexer import Lexer
from programy.aipl.reader import TextLineReader


class TestSyntax:

    def test_just_brackets(self):
        tokenizer = Tokenizer(Lexer(TextLineReader("""
            ()
        """)))
        assert tokenizer
        assert len(tokenizer.errors) == 1
        assert tokenizer.errors[0] == "Missing 'category', Line:2, Position:2, Token:')'"

    def test_valid_topic_that_pattern_template(self):

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
        assert len(tokenizer.errors) == 0
        assert tokenizer.length == 1
        assert tokenizer.tokens[0][0] == [(3, 4, '*')]
        assert tokenizer.tokens[0][1] == [(4, 4, '*')]
        assert tokenizer.tokens[0][2] == [(5, 4, 'HELLO'), (5, 5, '*')]
        assert tokenizer.tokens[0][3] == [(6, 4, 'Hi'), (6, 5, 'there!')]

    def test_valid_pattern_template(self):

        tokenizer = Tokenizer(Lexer(TextLineReader("""
        ( category (
                ( pattern (HELLO *) )
                ( template (Hi there!) )
            )
        )
        """)))
        assert tokenizer
        assert len(tokenizer.errors) == 0
        assert tokenizer.length == 1
        assert tokenizer.tokens[0][0] == [(-1, -1, '*')]
        assert tokenizer.tokens[0][1] == [(-1, -1, '*')]
        assert tokenizer.tokens[0][2] == [(3, 4, 'HELLO'), (3, 5, '*')]
        assert tokenizer.tokens[0][3] == [(4, 4, 'Hi'), (4, 5, 'there!')]

    def test_valid_multiple_categories(self):

        tokenizer = Tokenizer(Lexer(TextLineReader("""
            ( category (
                    ( pattern (HELLO *) )
                    ( template (Hi there!) )
                )
            )

            ( category (
                    ( pattern (HEY *) )
                    ( template (Hi there!) )
                )
            )
            """)))
        assert tokenizer
        assert len(tokenizer.errors) == 0
        assert tokenizer.length == 2

        assert tokenizer.tokens[0][0] == [(-1, -1, '*')]
        assert tokenizer.tokens[0][1] == [(-1, -1, '*')]
        assert tokenizer.tokens[0][2] == [(3, 4, 'HELLO'), (3, 5, '*')]
        assert tokenizer.tokens[0][3] == [(4, 4, 'Hi'), (4, 5, 'there!')]

        assert tokenizer.tokens[1][0] == [(-1, -1, '*')]
        assert tokenizer.tokens[1][1] == [(-1, -1, '*')]
        assert tokenizer.tokens[1][2] == [(9, 4, 'HEY'), (9, 5, '*')]
        assert tokenizer.tokens[1][3] == [(10, 4, 'Hi'), (10, 5, 'there!')]

    def test_valid_topic_categories_single(self):

        tokenizer = Tokenizer(Lexer(TextLineReader("""
        ( topic ( GREETING )
            ( category (
                    ( pattern (HELLO *) )
                    ( template (Hi there!) ) )
            )
        )
        """)))
        assert tokenizer
        print(tokenizer.errors)
        assert len(tokenizer.errors) == 0
        assert tokenizer.length == 1
        assert tokenizer.tokens[0][0] == [(2, 4, 'GREETING')]
        assert tokenizer.tokens[0][1] == [(-1, -1, '*')]
        assert tokenizer.tokens[0][2] == [(4, 4, 'HELLO'), (4, 5, '*')]
        assert tokenizer.tokens[0][3] == [(5, 4, 'Hi'), (5, 5, 'there!')]

    def test_valid_topic_categories_multiple(self):

        tokenizer = Tokenizer(Lexer(TextLineReader("""
        ( topic ( GREETING )
            ( category (
                ( pattern (HELLO *) )
                ( template (Hi there!) ) )
            )
            ( category (
                ( pattern (HEY *) )
                ( template (Well hello!) ) )
            )
        )
        """)))
        assert tokenizer
        assert len(tokenizer.errors) == 0
        assert tokenizer.length == 2

        assert tokenizer.tokens[0][0] == [(2, 4, 'GREETING')]
        assert tokenizer.tokens[0][1] == [(-1, -1, '*')]
        assert tokenizer.tokens[0][2] == [(4, 4, 'HELLO'), (4, 5, '*')]
        assert tokenizer.tokens[0][3] == [(5, 4, 'Hi'), (5, 5, 'there!')]

        assert tokenizer.tokens[1][0] == [(2, 4, 'GREETING')]
        assert tokenizer.tokens[1][1] == [(-1, -1, '*')]
        assert tokenizer.tokens[1][2] == [(8, 4, 'HEY'), (8, 5, '*')]
        assert tokenizer.tokens[1][3] == [(9, 4, 'Well'), (9, 5, 'hello!')]
