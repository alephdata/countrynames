import re

COLLAPSE = re.compile(r'\s+', re.U)
BRACKETED = re.compile(r'(\([^\(\)]*\)|\[[^\[\]]*\])')
WS = ' '

# Unicode character classes, see:
# http://www.fileformat.info/info/unicode/category/index.htm
CATEGORIES = {
    'C': None,
    'M': None,
    'Z': WS,
    'P': '',
    # 'S': WS
}


def normalise_name(country):
    pass
