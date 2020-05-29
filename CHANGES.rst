=======
CHANGES
=======


0.2.1 (2020-05-28)
------------------

- Fix an error message to refer to the righ type.

- Added a test to ensure SUM() works with arrays containing Excel data types.


0.2.0 (2020-05-28)
------------------

- Support for delayed argument execution by introducing expressions that can
  be evaluated when needed. This is required to support efficient logical
  operator implementations. For example, when an "if"-condition is true, the
  false value does not need to be computed.

- Implemented all Excel types.

  + Better control of logic differences between Python and Excel. (Compare
    with None and blank handling, for example.)

  + Tight control of type casting with very situation-specific edge case
    handling. (For example, when a string representing a boolean will evaluate
    as a boolean and when not. For example, `int(bool('False')) == 0` in Excel
    but `AND('False', True) == True`.

  + Make date/time its own type.

- Moved errors back into their own module.

- Moved criteria parsing into its own module.

- Made function signature validation and conversion much more consistent
  allowing a lot less error handling and data conversion in the function
  body.



0.1.0 (2020-05-25)
------------------

- Complete rewrite of library.

  * Introduced a function registry that can be used to extend the function
    library in third party software.

  * Removed excessive use of static methods and converted all Excel functions
    to simple Python functions (with some decorators).

  * Organized functions into categories based on Microsoft documentation.

  * Proper argument validation and conversion where supported.

  * Many functions are now much more flexible with their types and more
    correctly mimic Excel behavior.

  * Use of `dateutil` and `yearfrac` libraries to do complicated date
    calculations instead of implementing it from scratch.

  * Achieved 100% test coverage.


0.0.3b (2020-05-11)
-------------------

- Initial release.
