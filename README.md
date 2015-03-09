# gcontacts-extractor [![Build Status](https://travis-ci.org/desko27/gcontacts-extractor.svg?branch=master)](https://travis-ci.org/desko27/google-contacts-address-extractor) [![Codacy Badge](https://www.codacy.com/project/badge/8077cc0440db43709c6b554a2d51a3b6)](https://www.codacy.com/public/desko27/gcontacts-extractor)

## Usage

```
gcontacts-extractor.py [-s] [-k] (-f | <source-accounts> ...)
```

## Description

This script is intended for **extracting contact's addresses** from a specified
set of **Google Apps users**. You must have Google Apps with API enabled, and
set up the API Auth data on `google_apps_api_auth.ini`.

Output goes to the relative folder defined in `results_folder` value of `conf.ini`,
which is `extracted_addresses` by default.

## Options
  
```
-h --help
-s --separated  send output to separated files (per account)
-k --keep       keep previous results on the output folder
-f --from-file  get source accounts from file instead of from arguments
```
