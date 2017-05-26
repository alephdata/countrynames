# coding: utf-8
import countrynames

tests = [
    'Germany',
    'DE',
    'UK',
    u'Российская Федерация',
    'Rossiyskaya Federatsiya',
    'Tgermany',
    None
]

for test in tests:
    print [test, countrynames.to_code(test, fuzzy=False),
           countrynames.to_code(test)]
