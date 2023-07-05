from pygments.lexer import RegexLexer, bygroups
from pygments.token import *

class RefalLexer(RegexLexer):
    name = 'Refal'
    aliases = ['refal']
    filenames = ['*.ref']
    KEYWORDS = [] 
    def get_tokens_unprocessed(self, text):
        for index, token, value in super(RefalLexer,self).get_tokens_unprocessed(text):
            if token is Name and value in self.KEYWORDS:
                yield index, Keyword, value
            else:
                yield index, token, value
    tokens = {
        'root': [
            (r'\*.*?$', Comment.Singleline),
            (r'(\$ENTRY|\$EXTERN)?(\s*)([A-Z][a-zA-Z0-9]*)(\s*)(\{)', 
             bygroups(Name.Decorator,Whitespace,Name.Function,Whitespace,Punctuation), 'body'),
            (r'[\s]+', Whitespace),
            (r'/\*', Comment.Multiline, 'comment')
        ],
        'body': [
            (r'\}', Punctuation, '#pop'),
            (r'\s+', Whitespace),
            (r'/\*', Comment.Multiline, 'comment'),
            (r'(?=.)', Whitespace, 'lhs'),
        ],
        'comment': [
            (r'[^\*]+', Comment.Multiline),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'\*', Comment.Multiline)
        ],
        'lhs': [
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r'\(', Punctuation, 'paren-lhs'),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'[a-zA-Z][a-zA-Z0-9-_]*', Name.Constant),
            (r'\s+', Whitespace),
            (r'=', Punctuation, ('#pop', 'rhs'))
        ],
        'paren-lhs': [
            (r'\)', Punctuation, '#pop'),
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r'\(', Punctuation, '#push'),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'[a-zA-Z][a-zA-Z0-9-_]*', Name.Constant),
            (r'\s+', Whitespace)
        ],
        'rhs': [
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r"\(", Punctuation, 'paren-rhs'),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'(<)([A-Z][a-zA-Z0-9]*)(?=[<>\s])', bygroups(Punctuation,Name.Function), 'fun'),
            (r'[a-zA-Z0-9]+', Name.Constant),
            (r'\s+', Whitespace),
            (r';', Punctuation, '#pop')
        ],
        'paren-rhs': [
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r"\(", Punctuation, '#push'),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'(<)([A-Z][a-zA-Z0-9]*)(?=[<>\s])', bygroups(Punctuation,Name.Function), 'fun'),
            (r'[a-zA-Z][a-zA-Z0-9-_]*', Name.Constant),
            (r'\s+', Whitespace),
            (r'\)', Punctuation, '#pop')
        ],
        'fun': [
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r'>', Punctuation, '#pop'),
            (r"\(", Punctuation, 'paren-rhs'),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'(<)([A-Z][a-zA-Z0-9]*)(?=[<>\s])', bygroups(Punctuation,Name.Function), '#push'),
            (r'[a-zA-Z][a-zA-Z0-9-_]*', Name.Constant),
            (r'\s+', Whitespace)
        ],
        'string': [
            (r'\\.', String.Single),
            (r"'", String.Single, '#pop'),
            (r"[^'\\]", String.Single)
        ]
    }
