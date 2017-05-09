import os
import yaml
import logging
import Levenshtein
from normality import normalize
from pycountry import countries

log = logging.getLogger(__name__)

__all__ = ['to_code']

COUNTRY_NAMES = {}


def _normalize_name(country):
    """Clean up a country name before comparison."""
    return normalize(country, latinize=True)


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


def to_code(country_name, fuzzy=True):
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
    if code == 'FAIL':
        return None

    if code is None and fuzzy is True:
            code = _fuzzy_search(name)
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
