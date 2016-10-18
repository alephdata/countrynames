# coding: utf-8
import countrynames

tests = [
    'Germany',
    'DE'
]

for test in tests:
    print [test, countrynames.to_code(test)]
