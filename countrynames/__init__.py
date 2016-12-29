import six
import os
import yaml
import logging
import Levenshtein
from pycountry import countries
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


def _fuzzy_search(name):
    matches = set()
    for cand, code in COUNTRY_NAMES.items():
        if len(cand) <= 4:
            continue
        if cand in name:
            matches.add(code)
        elif Levenshtein.distance(name, cand) <= 2:
            matches.add(code)
    if len(matches) == 1:
        for match in matches:
            log.debug("Guessing country: %s -> %s", name, match)
            return match


def to_code(country_name):
    """Given a human name for a country, return its ISO two-digit code."""
    # Lazy load country list
    if not len(COUNTRY_NAMES):
        _load_data()
    name = _normalize_name(country_name)
    if name is None:
        return

    # Check if the input is actually an ISO code:
    upper = country_name.upper()
    if upper in COUNTRY_NAMES.values():
        return upper

    # Lookup
    code = COUNTRY_NAMES.get(name)
    if code is None:
        code = _fuzzy_search(name)
        COUNTRY_NAMES[name] = code
    if code == 'FAIL':
        return None
    if code is None:
        log.info("Unknown country: %s (searched: %s)", country_name, name)
        COUNTRY_NAMES[name] = 'FAIL'
    return code


def to_alpha_3(country_name):
    """Given a human name for a country, return its ISO three-digit code"""
    try:
        return countries.get(alpha_2=to_code(country_name)).alpha_3
    except LookupError:
        return None


def to_name(country_name):
    """Given a human name for a country, return its short name"""
    try:
        return countries.get(alpha_2=to_code(country_name)).name
    except LookupError:
        return None


def to_official_name(country_name):
    """Given a human name for a country, return its full official name"""
    try:
        country = countries.get(alpha_2=to_code(country_name))
        if hasattr(country, "official_name"):
            return country.official_name
        else:
            return country.name
    except LookupError:
        return None


def to_numeric(country_name):
    """Given a human name for a country, return its numeric code as a string"""
    try:
        return countries.get(alpha_2=to_code(country_name)).numeric
    except LookupError:
        return None
