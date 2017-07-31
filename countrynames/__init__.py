import os
import six
import yaml
import logging
import Levenshtein
from normality import normalize
from pycountry import countries
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


log = logging.getLogger(__name__)

__all__ = ['to_code', 'to_alpha_3', 'to_name', 'to_official_name',
           'to_numeric']

COUNTRY_NAMES = {}


def _normalize_name(country):
    """Clean up a country name before comparison."""
    norm = normalize(country, latinize=True)
    return six.text_type(norm)


def _load_data():
    """Load known aliases from a YAML file. Internal."""
    data_file = os.path.join(os.path.dirname(__file__), 'data.yaml')
    with open(data_file, 'r') as fh:
        for code, names in yaml.load(fh, Loader=Loader).items():
            code = code.strip().upper()
            COUNTRY_NAMES[_normalize_name(code)] = code
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


def to_code(country_name, fuzzy=False):
    """Given a human name for a country, return its ISO two-digit code.

    Arguments:
        ``fuzzy``: Try fuzzy matching based on Levenshtein distance.
    """
    # Lazy load country list
    if not len(COUNTRY_NAMES):
        _load_data()

    # shortcut before costly ICU stuff
    if isinstance(country_name, six.text_type):
        country_name = country_name.upper().strip()
        # Check if the input is actually an ISO code:
        if country_name in COUNTRY_NAMES.values():
            return country_name

    # Transliterate and clean up
    name = _normalize_name(country_name)
    if name is None:
        return

    # Direct look up
    code = COUNTRY_NAMES.get(name)
    if code == 'FAIL':
        return None

    # Find closest match with spelling mistakes
    if code is None and fuzzy is True:
        code = _fuzzy_search(name)
    return code


def to_alpha_3(country_name, fuzzy=False):
    """Given a human name for a country, return its ISO three-digit code.

    Arguments:
        ``fuzzy``: Try fuzzy matching based on Levenshtein distance.
    """
    try:
        code = to_code(country_name, fuzzy=fuzzy)
        if code == "EU":  # European Union
            return "EUU"
        elif code == "XK":  # Kosovo
            return "XKX"
        else:
            return countries.get(alpha_2=code).alpha_3
    except LookupError:
        return None


def to_name(country_name, fuzzy=False):
    """Given a human name for a country, return its short name.

    Arguments:
        ``fuzzy``: Try fuzzy matching based on Levenshtein distance.
    """
    try:
        return countries.get(alpha_2=to_code(country_name, fuzzy=fuzzy)).name
    except LookupError:
        return None


def to_official_name(country_name, fuzzy=False):
    """Given a human name for a country, return its full official name."""
    try:
        country = countries.get(alpha_2=to_code(country_name, fuzzy=fuzzy))
        if hasattr(country, "official_name"):
            return country.official_name
        else:
            return country.name
    except LookupError:
        return None


def to_numeric(country_name, fuzzy=False):
    """Given a human name for a country, return its numeric code as a string.

    Arguments:
        ``fuzzy``: Try fuzzy matching based on Levenshtein distance.
    """
    try:
        return countries.get(alpha_2=to_code(country_name,
                                             fuzzy=fuzzy)).numeric
    except LookupError:
        return None
