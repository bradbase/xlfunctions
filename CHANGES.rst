=======
CHANGES
=======


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
