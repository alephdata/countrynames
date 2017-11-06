# coding: utf-8
from countrynames import to_code, to_alpha_3


def test_to_code():
    assert to_code("Germany") == "DE"
    assert to_code("UK") == "GB"


def test_to_alpha_3():
    assert to_alpha_3("Germany") == "DEU"
    assert to_alpha_3("UK") == "GBR"


def test_unicode():
    assert to_code(u'Российская Федерация') == "RU"


def test_fuzzy_matching():
    assert to_code('Rossiyskaya Federatsiya', fuzzy=True) == "RU"
    assert to_code("Falklands Islands", fuzzy=True) == "FK"
    assert to_code("TGermany", fuzzy=True) == "DE"


def test_non_standard_codes():
    assert to_code("European Union") == "EU"
    assert to_alpha_3("European Union") == "EUU"
    assert to_code("Kosovo") == "XK"
    assert to_alpha_3("Kosovo") == "XKX"


def test_GB():
    assert to_code("Scotland") == "GB-SCT"
    assert to_code("Wales") == "GB-WLS"
    assert to_code("Northern Ireland") == "GB-NIR"
    assert to_code("Northern Ireland", fuzzy=True) == "GB-NIR"
    assert to_code(
        "United Kingdom of Great Britain and Northern Ireland") == "GB"
    assert to_code(
        "United Kingdom of Great Britain and Northern Ireland",
        fuzzy=True) == "GB"
