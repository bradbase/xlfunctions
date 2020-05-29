import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


TESTS_REQUIRE = [
    'coverage',
    'flake8',
    'mock',
    'pytest',
    'pytest-cov',
]


setup(
    name="xlfunctions",
    version='0.2.1',
    author="Bradley van Ree",
    author_email="brads@bradbase.net",
    description=(
        "Implemententation of Python equivalents of MS Excel functions."
    ),
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('CHANGES.rst')
        ),
    url="https://github.com/bradbase/xlfunctions",
    packages=find_packages(),
    license="GPL 3.0",
    keywords="Excel functions",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=[
        'numpy',
        'pandas',
        'numpy_financial',
        'python-dateutil',
        'yearfrac',
    ],
    extras_require=dict(
        test=TESTS_REQUIRE,
        build=[
            'pip-tools',
        ],
    ),
    python_requires='>=3.7',
    tests_require=TESTS_REQUIRE,
    include_package_data=True,
    zip_safe=False,
)
