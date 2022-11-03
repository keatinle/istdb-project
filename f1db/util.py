# fancy html formatting
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter

def sql_html_formatter(sql):
    return highlight(sql, SqlLexer(), HtmlFormatter())