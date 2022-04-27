import os
import yaml
import logging
import _pickle as CPickle
from typing import List, Dict, Set, Tuple
from collections import defaultdict

from countrynames.util import process_data

log = logging.getLogger("countrynames.compile")
CODE_DIR = os.path.dirname(__file__)


def load_yaml_data() -> Dict[str, List[str]]:
    data = defaultdict(list)
    data_file = os.path.join(CODE_DIR, "data.yaml")
    with open(data_file, "r", encoding="utf-8") as fh:
        for code, names in yaml.safe_load(fh).items():
            data[code].extend(names)
    return data

def write_pickle(data: Dict[str, List[str]]) -> None:
    pickle_file = os.path.join(CODE_DIR, "data.pickle")
    with open(pickle_file, "wb") as fh:
        CPickle.dump(data, fh)

def write_python(data: Dict[str, List[str]]) -> None:
    python_file = os.path.join(CODE_DIR, "data.py")
    with open(python_file, "w", encoding="utf-8") as pyfh:
        pyfh.write("# generated file, do not edit.\n")
        pyfh.write("from typing import Dict, List\n\n")
        pyfh.write("DATA: Dict[str, List[str]] = {}\n")
        for code, names in data.items():
            code = code.strip().upper()
            pyfh.write("DATA[%r] = %r\n" % (code, names))


def validate_data(data: Dict[str, List[str]]) -> None:
    """Run a check on the country name database."""
    mappings: Dict[str, Set[Tuple[str, str]]] = {}
    for code, norm, original in process_data(data):
        mappings.setdefault(norm, set())
        mappings[norm].add((code, original))
    for norm, assigned in mappings.items():
        countries = set([c for (c, _) in assigned])
        if len(countries) == 1:
            continue
        log.warning("Ambiguous string [%s]: %r", norm, assigned)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    data = load_yaml_data()
    validate_data(data)
    write_python(data)
    names = {}
    for code, norm, _ in process_data(data):
        names[norm] = code
    write_pickle(names)
