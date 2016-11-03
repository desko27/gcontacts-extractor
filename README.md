# gcontacts-extractor

[![Build Status](https://travis-ci.org/desko27/gcontacts-extractor.svg?branch=master)](https://travis-ci.org/desko27/gcontacts-extractor)
[![Codacy Badge](https://www.codacy.com/project/badge/8077cc0440db43709c6b554a2d51a3b6)](https://www.codacy.com/public/desko27/gcontacts-extractor)
[![Gitter chat](https://badges.gitter.im/desko27/gcontacts-extractor.png)](https://gitter.im/desko27/gcontacts-extractor "Gitter chat")

This script is intended for extracting contact's addresses from a specified
set of Google Apps users. To do that, it connects to the
[Google Contacts API version 3.0](https://developers.google.com/google-apps/contacts/v3/)
and iterates over the passed list of accounts.

## Usage

```
gcontacts-extractor.py [-d=<domain>] [-s] [-k] (-f | <source-accounts> ...)
```

## Howto

1. [Create a service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#creatinganaccount) in Google Apps console and paste `service_account_keys.json` in the settings folder.
2. [Authorize the contacts scope](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority) for the service account: `https://www.google.com/m8/feeds/`.
3. Copy sample config files and remove their `.sample` extension.
4. Set default_domain in `conf.ini` as your Google Apps domain.
5. Execute `gcontacts-extractor.py -s bob jack sally` __note*__.
6. You've got `bob.txt`, `jack.txt` and `sally.txt` text files containing all of their mail addresses.

__note*__ → the domain here is implied since it is previously defined in `conf.ini`, so when you write `bob` the script is actually understanding `bob@yourdomain.com` and so on.

## Options
  
```
-h --help
-d --domain=<domain>  override default domain
-s --separated        send output to separated files (per account)
-k --keep             keep previous results on the output folder
-f --from-file        get source accounts from file instead of from arguments
```
