import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xlfunctions",
    version="0.0.2b",
    author="Bradley van Ree",
    author_email="brads@bradbase.net",
    description="xlfunctions implements Python equivalents of MS Excel formulas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bradbase/xlfunctions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
            'numpy >= 1.18.1',
            'pandas >= 1.0.1',
            'numpy_financial >= 1.0.0'
        ],
    python_requires='>=3.7.6',
)
