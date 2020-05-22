from setuptools import setup, find_packages


with open("README.md", "r") as fp:
    long_description = fp.read()


TESTS_REQUIRE = [
    'coverage',
    'zope.testrunner',
    'flake8',
    'mock',
]



setup(
    name="xlfunctions",
    version="0.0.3b",
    author="Bradley van Ree",
    author_email="brads@bradbase.net",
    description=(
        "Implemententation of Python equivalents of MS Excel functions."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bradbase/xlfunctions",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=[
        'numpy >= 1.18.1',
        'pandas >= 1.0.1',
        'numpy_financial >= 1.0.0',
        'yearfrac',
    ],
    extras_require=dict(
        test=TESTS_REQUIRE,
    ),
    python_requires='>=3.7.6',
    tests_require=TESTS_REQUIRE,
)
