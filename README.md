# gcontacts-extractor
## Google Contacts Address Extractor

[![Build Status](https://travis-ci.org/desko27/gcontacts-extractor.svg?branch=master)](https://travis-ci.org/desko27/google-contacts-address-extractor)

:notebook: Extracts contact's addresses from a specified set of Google Apps users.

```
This script is intended for extracting contact's addresses from a specified
set of Google Apps users. You must have Google Apps with API enabled, and
set up the API Auth data on the corresponding file.

Output goes to the relative folder defined in results_folder value of conf.ini

Usage: gcontacts-extractor.py [-s] [-k] (-f | <source-accounts> ...)
  
Options:
  -h --help
  -s --separated  send output to separated files (per account)
  -k --keep       keep previous results on the output folder
  -f --from-file  get source accounts from file instead of from arguments
```
