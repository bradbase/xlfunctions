===========
XLFunctions
===========

.. image:: https://travis-ci.org/bradbase/xlfunctions.png?branch=master
   :target: https://travis-ci.org/bradbase/xlfunctions

.. image:: https://coveralls.io/repos/github/bradbase/xlfunctions/badge.svg?branch=master
   :target: https://coveralls.io/github/bradbase/xlfunctions?branch=master

.. image:: https://img.shields.io/pypi/v/xlfunctions.svg
    :target: https://pypi.python.org/pypi/xlfunctions

.. image:: https://img.shields.io/pypi/pyversions/xlfunctions.svg
    :target: https://pypi.python.org/pypi/xlfunctions/

.. image:: https://img.shields.io/pypi/status/xlfunctions.svg
    :target: https://pypi.org/project/xlfunctions/
    :alt: Package stability

A collection of classes which implement functions as used in Microsoft
Excel. The intent is to be a definitive library to support evaluating Excel
calculations.

There are a number of solutions being developed in the Python universe which
are writing their own implementations of the same functions. Often those
implementations are simply wrapping pandas, numpy or scipy. Although
potentially fit for purpose in those solutions, the calculated result may not
necessarily agree with Excel.

There are also a handful of libraries to be found which have attempted a
universal Python implementation of Excel functions however as they aren't
being actively used by a library they appear to be abandoned reasonably
rapidly. xlfunctions is being used by
`xlcalcualtor <https://github.com/bradbase/xlcalculator>`_ (an attempted
re-write of `Koala2 <https://github.com/vallettea/koala>`_ and, in turn,
`FlyingKoala <https://github.com/bradbase/flyingkoala>`_).

Excel occasionally does unusual things while calculating which may not always
align with what is accepted outside the realms of Excel. With this in mind it
is common that numpy, scipy or pandas libraries may not calculate a result
which agrees with Excel. This is especially true of Excel's date
handling. This library attempts to take care to return results as close as
possible to what Excel would expect. **If you want to align perfectly with
Excel, please read the discussion on Excel number precision (below)**


Supported Functions
-------------------

* ABS
* AVERAGE
* CHOOSE
* CONCAT
* COUNT
* COUNTA
* DATE
* IRR
* LN
    - Python Math.log() differs from Excel LN. Currently returning Math.log()
* MAX
* MID
* MIN
* MOD
* NPV
* PMT
* POWER
* RIGHT
* ROUND
* ROUNDDOWN
* ROUNDUP
* SLN
* SQRT
* SUM
* SUMPRODUCT
* TODAY
* VLOOKUP
    - Exact match only
* XNPV
* YEARFRAC
    - Basis 1, Actual/actual, is only within 3 decimal places


Run Tests
---------

Setup your environment::

  virtualenv -p 3.7 ve
  ve/bin/pip install -e .[test]

From the root xlfunctions directory::

  ve/bin/python -m unittest discover -p "test_*.py"

Or simply run tox::

  tox

Adding/Registering Excel Functions
----------------------------------

Excel functions can be added by any code using the the
``xlfunctions.xl.register()`` decorator. Here is a simple example:

.. code-block:: Python

  from xlfunctions import xl

  @xl.register()
  @xl.validate_args
  def ADDONE(num: xl.Number):
      return num + 1

The `v@xl.alidate_args` decorator will ensure that the annotated arguments are
converted and validated. For example, even if you pass in a string, it is
converted to a number (in typical Excel fashion):

.. code-block:: Python

  >>> ADDONE(1):
  2
  >>> ADDONE('1'):
  2

If you would like to contribute functions, please create a pull request. All
new functions should be accompanied by sufficient tests to cover the
functionality.


Excel number precision
----------------------

Excel number precision is a complex discussion.

It has been discussed in a `Wikipedia
page <https://en.wikipedia.org/wiki/Numeric_precision_in_Microsoft_Excel>`_.

The fundamentals come down to floating point numbers and a contention between
how they are represented in memory Vs how they are stored on disk Vs how they
are presented on screen. A `Microsoft
article <https://www.microsoft.com/en-us/microsoft-365/blog/2008/04/10/understanding-floating-point-precision-aka-why-does-excel-give-me-seemingly-wrong-answers/>`_
explains the contention.

This project is attempting to take care while reading numbers from the Excel
file to try and remove a variety of representation errors.

Further work will be required to keep numbers in-line with Excel throughout
different transformations.

From what I can determine this requires a low-level implementation of a
numeric datatype (C or C++, Cython??) to replicate its behaviour. Python
built-in numeric types don't replicate appropriate behaviours.
