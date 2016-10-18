import six
import os
import yaml
import logging
from unicodedata import normalize, category

log = logging.getLogger(__name__)
__all__ = ['to_code']

# Unicode character classes, see:
# http://www.fileformat.info/info/unicode/category/index.htm
CATEGORIES = {
    'C': None,
    'M': None,
    'Z': ' ',
    'P': None,
    'S': ' '
}
COUNTRY_NAMES = {}


def _normalize_name(country):
    """Clean up a country name before comparison."""
    if country is None:
        return
    if not isinstance(country, six.text_type):
        country = six.text_type(country)
    word = []
    for character in normalize('NFKD', country.lower()):
        cat = category(character)[0]
        character = CATEGORIES.get(cat, character)
        if character is None:
            continue
        word.append(character)
    words = [w for w in ''.join(word).split(' ') if len(w)]
    text = ' '.join(sorted(set(words)))
    if len(text):
        return text


def _load_data():
    """Load known aliases from a YAML file. Internal."""
    data_file = os.path.join(os.path.dirname(__file__), 'data.yaml')
    with open(data_file, 'r') as fh:
        for code, names in yaml.load(fh).items():
            code = code.strip().upper()
            for name in names:
                COUNTRY_NAMES[_normalize_name(name)] = code


def to_code(country_name):
    """Given a human name for a country, return its ISO two-digit code."""
    # Lazy load country list
    if not len(COUNTRY_NAMES):
        _load_data()
    name = _normalize_name(country_name)

    # Check if the input is actually an ISO code:
    upper = country_name.upper()
    if upper in COUNTRY_NAMES.values():
        return upper

    # Lookup
    code = COUNTRY_NAMES.get(name)
    if code is None:
        log.info("Unknown country name: %s (searched: %s)", country_name, name)
    return code
