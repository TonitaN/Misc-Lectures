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
            (r'(\$EXTERN)(\s+)([A-Z][a-zA-Z0-9_-]*)',
             bygroups(Name.Decorator,Whitespace,Name.Function), 'dependencies'),
            (r'(\$ENTRY )?(\s*)([A-Z][a-zA-Z0-9_-]*)(\s*)(\{)', 
             bygroups(Name.Decorator,Whitespace,Name.Function,Whitespace,Punctuation), 'body'),
            (r'[\s]+', Whitespace),
            (r'/\*', Comment.Multiline, 'comment'),
            (r'(?=.)', Whitespace, 'bare_expr')
        ],
        'dependencies' : [
            (r'/\*', Comment.Multiline, 'comment'),
            (r'[\s]+', Whitespace),
            (r';', Punctuation, '#pop'),
            (r'(,)(\s*)',
             bygroups(Punctuation,Whitespace), 'force-dep')
        ],
        'force-dep' : [
            (r'/\*', Comment.Multiline, 'comment'),
            (r'[\s]+', Whitespace),
            (r'[A-Z][a-zA-Z0-9_-]*',Name.Function, '#pop')
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
            (r'([1-9][0-9]*|0)', Number.Integer),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'[a-zA-Z][a-zA-Z0-9-_]*', Name.Constant),
            (r'\s+', Whitespace),
            (r'=', Punctuation, ('#pop', 'rhs')),
            (r',', Punctuation, 'irhs'),
        ],
        'irhs': [
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r"\(", Punctuation, 'paren-rhs'),
            (r'([1-9][0-9]*|0)', Number.Integer),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'(<)([A-Z][a-zA-Z0-9]*)(?=[<>\s])', bygroups(Punctuation,Name.Function), 'fun'),
            (r'[a-zA-Z0-9]+', Name.Constant),
            (r'\s+', Whitespace),
            (r':', Punctuation, ('#pop','blockVlhs')),
        ],
        'blockVlhs': [
            (r'/\*', Comment.Multiline, 'comment'),
            (r'\s+', Whitespace),
            (r'\{', Punctuation, ('#pop','#pop','block_body')),
            (r'(?=.)', Whitespace, '#pop')            
        ],
        'block_body': [
            (r'\};', Punctuation, '#pop'),
            (r'\s+', Whitespace),
            (r'/\*', Comment.Multiline, 'comment'),
            (r'(?=.)', Whitespace, 'lhs'),
        ],
        'paren-lhs': [
            (r'\)', Punctuation, '#pop'),
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r'([1-9][0-9]*|0)', Number.Integer),
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
            (r'([1-9][0-9]*|0)', Number.Integer),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'(<)([A-Z][a-zA-Z0-9_-]*)(?=[<>\s])', bygroups(Punctuation,Name.Function), 'fun'),
            (r'[a-zA-Z0-9]+', Name.Constant),
            (r'\s+', Whitespace),
            (r';', Punctuation, '#pop')
        ],
        'bare_expr': [
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r"\(", Punctuation, 'paren-expr'),
            (r'([1-9][0-9]*|0)', Number.Integer),
            (r'(#[ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'(<)([A-Z][a-zA-Z0-9_-]*)(?=[<>\s])', bygroups(Punctuation,Name.Function), 'fun-expr'),
            (r'[a-zA-Z][a-zA-Z0-9]*', Name.Constant),
            (r'\s+', Whitespace),
            (r'$', Whitespace, '#pop')
        ],
        'paren-rhs': [
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r"\(", Punctuation, '#push'),
            (r'([1-9][0-9]*|0)', Number.Integer),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'(<)([A-Z][a-zA-Z0-9_-]*)(?=[<>\s])', bygroups(Punctuation,Name.Function), 'fun'),
            (r'[a-zA-Z][a-zA-Z0-9-_]*', Name.Constant),
            (r'\s+', Whitespace),
            (r'\)', Punctuation, '#pop')
        ],
        'fun': [
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r'>', Punctuation, '#pop'),
            (r"\(", Punctuation, 'paren-rhs'),
            (r'([1-9][0-9]*|0)', Number.Integer),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'(<)([A-Z][a-zA-Z0-9_-]*)(?=[<>\s])', bygroups(Punctuation,Name.Function), '#push'),
            (r'[a-zA-Z][a-zA-Z0-9-_]*', Name.Constant),
            (r'\s+', Whitespace)
        ],
        'paren-expr': [
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r"\(", Punctuation, '#push'),
            (r'([1-9][0-9]*|0)', Number.Integer),
            (r'(#[ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'(<)([A-Z][a-zA-Z0-9_-]*)(?=[<>\s])', bygroups(Punctuation,Name.Function), 'fun'),
            (r'[a-zA-Z][a-zA-Z0-9-_]*', Name.Constant),
            (r'\s+', Whitespace),
            (r'\)', Punctuation, '#pop')
        ],
        'fun-expr': [
            (r'/\*', Comment.Multiline, 'comment'),
            (r"'", String.Single, 'string'),
            (r'>', Punctuation, '#pop'),
            (r"\(", Punctuation, 'paren-rhs'),
            (r'([1-9][0-9]*|0)', Number.Integer),
            (r'(#[ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'([ets]\.)([a-zA-Z0-9_-]+)',
             bygroups(Keyword.Reserved,Name.Variable)),
            (r'(<)([A-Z][a-zA-Z0-9_-]*)(?=[<>\s])', bygroups(Punctuation,Name.Function), '#push'),
            (r'[a-zA-Z][a-zA-Z0-9-_]*', Name.Constant),
            (r'\s+', Whitespace)
        ],
        'string': [
            (r'\\.', String.Single),
            (r"'", String.Single, '#pop'),
            (r"[^'\\]", String.Single)
        ]
    }
