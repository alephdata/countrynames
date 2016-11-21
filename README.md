# countrynames

This library helps with the mapping of country names to their respective
ISO 3166-1 alpha-2, alpha-3, and numeric codes or official names. The idea is
to incorporate common names for countries, and even some limited misspellings,
as they occur in source data.

## Usage

```python
import countrynames

assert 'DE' == countrynames.to_code('Germany')
assert 'DE' == countrynames.to_code('Bundesrepublik Deutschland')
assert 'DE' == countrynames.to_code('DE')
assert 'Germany' == countrynames.to_name('Deutschland')
assert 'Federal Republic of Germany' == countrynames.to_official_name('Deutschland')
assert 'DEU' == countrynames.to_alpha_3('Germany')
assert '004' == countrynames.to_numeric('Afghanistan')
```

## Non-standard countries

* ``XK`` - Kosovo
* ``EU`` - European Union

## License

The MIT License (MIT)

Copyright (c) 2016 Friedrich Lindenberg

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
