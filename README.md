# gcontacts-extractor

[![Build Status](https://travis-ci.org/desko27/gcontacts-extractor.svg?branch=master)](https://travis-ci.org/desko27/google-contacts-address-extractor)
[![Codacy Badge](https://www.codacy.com/project/badge/8077cc0440db43709c6b554a2d51a3b6)](https://www.codacy.com/public/desko27/gcontacts-extractor)

## Usage

```
gcontacts-extractor.py [-s] [-k] (-f | <source-accounts> ...)
```

## Howto

1. Remove `.sample` extension from sample config files.
1. Set consumer_key, consumer_secret and admin_username on `google_apps_api_auth.ini`.
2. Execute `gcontacts-extractor.py bob jack sally`.
3. You've got `bob.txt`, `jack.txt` and `sally.txt` text files containing all of their mail addresses.

## Options
  
```
-h --help
-s --separated  send output to separated files (per account)
-k --keep       keep previous results on the output folder
-f --from-file  get source accounts from file instead of from arguments
```
