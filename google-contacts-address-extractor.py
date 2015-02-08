#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
#  - Author:    desko27
#  - Email:     desko27@gmail.com
#  - Version:   1.0.2
#  - Created:   2015/01/28
#  - Updated:   2015/02/08
# ----------------------------------------------------------------------------
# This script is intended for extracting contact's addresses from a specified
# set of Google Apps users. You must have Google Apps with API enabled, and
# set up the API Auth data on the corresponding file.

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
	
	# retrieve config values
	files = Config('conf.ini').files
	auth = Config(files.google_apps_api_auth).auth
	
	# list managers
	lm_exclusions = ListManager(file = files.exclusions)
	lm_source = ListManager(file = files.source_accounts)
	lm_export = ListManager(file = files.extracted_addresses, load = False)
	
	# google auth
	google = GoogleAuth(auth.consumer_key, auth.consumer_secret)
	
	# query conditions
	query = gdata.contacts.client.ContactsQuery()
	query.max_results = maxint
	
	# load & iterate over accounts
	accounts = lm_source.load()
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
					
		addresses = list(set(addresses)) # unique elements
		
		print '(%i)' % len(addresses)
		lm_export.list += addresses
	
	# save the extracted addresses
	lm_export.unique_elements()
	lm_export.save()
	
	# finished
	print '\nFinished! - (%s) TOTAL unique addresses.' % len(lm_export.list)
	