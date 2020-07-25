from countrynames import to_code, to_code_3


def test_to_code():
    assert to_code("Germany") == "DE"
    assert to_code("UK") == "GB"
    assert to_code("Nothing") is None


def test_to_code_3():
    assert to_code_3("Germany") == "DEU"
    assert to_code_3("UK") == "GBR"
    assert to_code_3("Nothing") is None


def test_unicode():
    assert to_code(u"Российская Федерация") == "RU"


def test_fuzzy_matching():
    assert to_code("Rossiyskaya Federacia", fuzzy=True) == "RU"
    assert to_code("Falklands Islands", fuzzy=True) == "FK"
    assert to_code("TGermany", fuzzy=True) == "DE"


def test_non_standard_codes():
    assert to_code("European Union") == "EU"
    assert to_code_3("European Union") == "EUU"
    assert to_code("Kosovo") == "XK", to_code("Kosovo")
    assert to_code_3("Kosovo") == "XKX"


def test_GB():
    assert to_code("Scotland") == "GB-SCT"
    assert to_code("Wales") == "GB-WLS"
    assert to_code("Northern Ireland") == "GB-NIR"
    assert to_code("Northern Ireland", fuzzy=True) == "GB-NIR"
    text = "United Kingdom of Great Britain and Northern Ireland"
    assert to_code(text) == "GB"
    text = "United Kingdom of Great Britain and Northern Ireland"
    assert to_code(text, fuzzy=True) == "GB"
