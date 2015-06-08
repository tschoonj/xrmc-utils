## Installation instructions

To use these Perl scripts:

````bash
perl Makefile.PL
make
make test
make install
````

If `make test` fails then you will need to install the Perl modules `Syntax::Keyword::Junction` and/or `Scalar::Util` using CPAN or your system's package manager.

## Uninstall

Uninstall the Perl scripts using the `pm-uninstall` utility (can be installed using CPAN):

````bash
pm-uninstall xrmc
````

