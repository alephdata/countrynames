import os
import yaml


data_file = os.path.join(os.path.dirname(__file__), 'data.yaml')
with open(data_file, 'r') as fh:
    data = yaml.load(fh)

COUNTRY_NAMES = {}

for code, names in data.get('names', []):
    code = code.strip().upper()
    COUNTRY_NAMES[code] = names
