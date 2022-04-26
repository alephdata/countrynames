import os
import yaml
import babel
import pycountry
from collections import defaultdict

data = defaultdict(list)
data_file = os.path.join(os.path.dirname(__file__), "countrynames", "data.yaml")
with open(data_file, "r") as fh:
    for code, names in yaml.load(fh).items():
        data[code].extend(names)

for country in pycountry.countries:
    cc = country.alpha2
    data[cc].append(country.name)
    data[cc].append(country.alpha3)
    if hasattr(country, "official_name"):
        data[cc].append(country.official_name)
    for loc in babel.localedata.locale_identifiers():
        name = babel.Locale(loc).territories.get(cc)
        if name is not None:
            data[cc].append(name)

    data[cc] = list(set(data[cc]))

data_file = os.path.join(os.path.dirname(__file__), "countrynames", "data.yaml")
with open(data_file, "w") as fh:
    yaml.safe_dump(dict(data), fh, default_flow_style=False, allow_unicode=True)
