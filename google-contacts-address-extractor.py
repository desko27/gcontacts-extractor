#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
#  - Author:    desko27
#  - Email:     desko27@gmail.com
#  - Version:   1.1.0
#  - Created:   2015/01/28
#  - Updated:   2015/02/18
# ----------------------------------------------------------------------------
"""This script is intended for extracting contact's addresses from a specified
set of Google Apps users. You must have Google Apps with API enabled, and
set up the API Auth data on the corresponding file.

Output goes to the relative folder defined in results_folder value of conf.ini

Usage: ~extractor.py [-s] [-k] (-f | <source-accounts> ...)
  
Options:
  -h --help
  -s --separated  send output to separated files (per account)
  -k --keep       keep previous results on the output folder
  -f --from-file  get source accounts from file instead of from arguments
  
"""

from docopt import docopt
from os import listdir, remove
from os.path import join, isfile
from sys import maxint

# google api
import gdata.contacts.data
import gdata.contacts.client

# custom classes
from class_ListManager import ListManager
from class_GoogleAuth import GoogleAuth
from class_Config import Config, conf_exists

# ---------------------------------------------------------------------------
# program
# ---------------------------------------------------------------------------
if __name__ == '__main__':

	# retrieve arguments
	args = docopt(__doc__)
	
	# retrieve config values
	files = Config('conf.ini').files
	auth = Config(files.google_apps_api_auth).auth
	
	# remove previous results on results folder
	if not args['--keep']:
		for f in listdir(files.results_folder):
			element = join(files.results_folder, f)
			if isfile(element): remove(element)
	
	# list managers
	lm_exclusions = ListManager(file = files.exclusions)
	lm_source = ListManager(file = files.source_accounts)
	lm_export = ListManager(file = join(files.results_folder, files.results_file), load = False)
	
	# google auth
	google = GoogleAuth(auth.consumer_key, auth.consumer_secret)
	
	# query conditions
	query = gdata.contacts.client.ContactsQuery()
	query.max_results = maxint
	
	# load & iterate over accounts
	accounts = lm_source.load() if args['--from-file'] else args['<source-accounts>']
	exclusions = lm_exclusions.load()
	
	print 'Processing accounts...\n'
	for account in accounts:
		
		print ' >> %s' % account,
		
		gd_client = gdata.contacts.client.ContactsClient(domain = google.consumer_key, source='google-contacts-address-extractor')
		gd_client.auth_token = google.get_token(account)
		try: feed = gd_client.GetContacts(q = query)
		except: print '-Error-'; continue
		if not feed.entry: continue
		
		addresses = []
		for i, entry in enumerate(feed.entry):
			for email in entry.email:
				
				for exclusion in exclusions:
					if exclusion.startswith('@') and email.address.endswith(exclusion): break
					elif email.address == exclusion: break
				else:
					addresses.append(email.address)
					
		lm_acc_export = ListManager(file = join(files.results_folder, '%s.txt' % account), load = False)
		lm_acc_export.list = addresses
		lm_acc_export.unique_elements()
		if args['--separated']: lm_acc_export.save()
		
		print '(%i)' % len(addresses)
		lm_export.list += addresses
	
	# save the total extracted addresses
	lm_export.unique_elements()
	if not args['--separated']: lm_export.save()
	
	# finished
	print '\nFinished! - (%s) TOTAL unique addresses.' % len(lm_export.list)
	