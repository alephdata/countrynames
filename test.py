# coding: utf-8
import countrynames

tests = [
    'Germany',
    'DE',
    'UK',
    u'Российская Федерация',
    'Rossiyskaya Federatsiya',
    'Tgermany',
    'European Union',
    'Kosovo',
    None
]

print("No fuzzy matching:")
for test in tests:
    print([test,
           countrynames.to_code(test),
           countrynames.to_alpha_3(test),
           countrynames.to_name(test),
           countrynames.to_official_name(test),
           countrynames.to_numeric(test)
          ])

print("With fuzzy matching:")
for test in tests:
    print([test,
           countrynames.to_code(test, fuzzy=True),
           countrynames.to_alpha_3(test, fuzzy=True),
           countrynames.to_name(test, fuzzy=True),
           countrynames.to_official_name(test, fuzzy=True),
           countrynames.to_numeric(test, fuzzy=True)
        ])
