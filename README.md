
# XLFunctions

A collection of classes which implement functions as used in Microsoft Excel. The intent is to be a definitive library to support evaluating Excel calculations.

There are a number of solutions being developed in the Python universe which are writing their own implementations of the same functions. Often those implementations are simply wrapping pandas, numpy or scipy. Although potentially fit for purpose in those solutions, the calculated result may not necessarily agree with Excel.

There are also a handful of libraries to be found which have attempted a universal Python implementation of Excel functions however as they aren't being actively used by a library they appear to be abandoned reasonably rapidly. xlfunctions is being used by (xlcalcualtor)[https://github.com/bradbase/xlcalculator] (an attempted re-write of (Koala2)[https://github.com/vallettea/koala] and, in turn, (FlyingKoala)[https://github.com/bradbase/flyingkoala].

Excel occasionally does unusual things while calculating which may not always align with what is accepted outside the realms of Excel. With this in mind it is common that numpy, scipy or pandas libraries may not calculate a result which agrees with Excel. This is especially true of Excel's date handling. This library attempts to take care to return results as close as possible to what Excel would expect. **If you want to align perfectly with Excel, please read the discussion on Excel number precision (below)**


# Supported Functions
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


# Run tests
From the root xlfunctions directory
```python
python -m unittest discover -p "*_test.py"
```


# How to add Excel functions
Excel function support can be easily added to xlfunctions.

Do the git things.. (fork, clone, branch. checkout the new branch) and then;
- Write a class for the function in xlfunctions. Use existing supported function classes as template examples.
- Add the function name and related class to excel_lib.py SUPPORTED_FUNCTIONS dict
- Add the class to xlfunctions\\\_\_init\_\_.py
- Write a test for it in tests. Use existing tests as template examples. Often a great place for example test ideas is found on the Microsoft Office Excel help page for that function.
- Update the README.md to state that function is supported.
- Put your code, tests and doco forward as a pull request.


# Excel number precision
Excel number precision is a complex discussion.

It has been discussed in a (Wikipedia page)[https://en.wikipedia.org/wiki/Numeric_precision_in_Microsoft_Excel].

The fundamentals come down to floating point numbers and a contention between how they are represented in memory Vs how they are stored on disk Vs how they are presented on screen. A (Microsoft article)[https://www.microsoft.com/en-us/microsoft-365/blog/2008/04/10/understanding-floating-point-precision-aka-why-does-excel-give-me-seemingly-wrong-answers/] explains the contention.

This project is attempting to take care while reading numbers from the Excel file to try and remove a variety of representation errors.

Further work will be required to keep numbers in-line with Excel throughout different transformations.

From what I can determine this requires a low-level implementation of a numeric datatype (C or C++, Cython??) to replicate its behaviour. Python built-in numeric types don't replicate appropriate behaviours.


# TODO
- Improve testing, broadening test cases, testing for errors
- Support more functions
