from setuptools import setup, find_packages


setup(
    name='countrynames',
    version='1.1.1',
    description="A library to map country names to ISO codes.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    keywords='names countries iso country',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/occrp/countrynames',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
    namespace_packages=[],
    package_data={
        '': ['countrynames/data.yaml']
    },
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        'normality',
        'unidecode',
        'python-Levenshtein',
        'pycountry',
        'pyyaml',
        'six'
    ],
    tests_require=[
    ],
    entry_points={
    }
)
