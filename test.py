# coding: utf-8
import countrynames

tests = [
    'Germany',
    'DE',
    None
]

for test in tests:
    print [test, countrynames.to_code(test)]
