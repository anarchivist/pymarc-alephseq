# pymarc-alephseq

Provides an iterator class for reading a file of MARC records in Aleph
Sequential format, used by Ex Libris's Aleph ILS using the APIs provided
by [pymarc](https://github.com/edsu/pymarc). The initial implementation was based on a Perl implementation (`MARC::File::AlephSeq`) developed by
Tim Prettyman at the University of Michigan.

Thus far, it has not been maintained for Python 3, although it still appears to
work under Python 2.7.14 and pymarc 3.13. I don't use this code anymore,
although I may try to port it to Python 3 as an exercise.
