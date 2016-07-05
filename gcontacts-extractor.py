#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
#  - Author:    desko27
#  - Email:     desko27@gmail.com
#  - Version:   2.1.0
#  - Created:   2015/01/28
#  - Updated:   2016/06/29
# ----------------------------------------------------------------------------
"""This script is intended for extracting contact's addresses from a specified
set of Google Apps users. See https://github.com/desko27/gcontacts-extractor
for a howto about configuring your Google Apps environment and running this
script with it.

Output goes to the relative folder defined in output_folder value of conf.ini

Usage: gcontacts-extractor.py [-d=<domain>] [-s] [-k] (-f | <source-accounts> ...)
  
Options:
  -h --help
  -d --domain=<domain>  override default domain
  -s --separated        send output to separated files (per account)
  -k --keep             keep previous results on the output folder
  -f --from-file        get source accounts from file instead of from arguments
  
"""

from docopt import docopt
from os import mkdir, listdir, remove
from os.path import join, isfile, exists
from sys import maxint

# google api
import gdata.contacts.data
import gdata.contacts.client
from oauth2client.service_account import ServiceAccountCredentials

# local modules
from libs.ListManager import ListManager
from libs.Config import Config

# ---------------------------------------------------------------------------
# program
# ---------------------------------------------------------------------------
if __name__ == '__main__':

    # retrieve arguments
    args = docopt(__doc__)
    
    # retrieve config values
    conf = Config('settings/conf.ini')
    files = conf.files
    auth = conf.auth

    # override domain if it's specified
    domain = args['--domain'] if args['--domain'] != None else auth.default_domain
    
    # create output folders if they don't exist
    final_output_folder = join(files.output_folder, domain)
    if not exists(files.output_folder): mkdir(files.output_folder)
    if not exists(final_output_folder): mkdir(final_output_folder)
    
    # remove previous results on output folder
    if not args['--keep']:
        for f in listdir(final_output_folder):
            element = join(final_output_folder, f)
            if isfile(element): remove(element)
    
    # list managers
    lm_exclusions = ListManager(file = files.exclusions)
    lm_source = ListManager(file = files.source_accounts)
    lm_export = ListManager(file = join(final_output_folder, files.output_file), load = False)
    
    # google auth -> use the service account
    # (should be authorised to use 'https://www.google.com/m8/feeds/' scope from google api console)
    scopes = ['https://www.google.com/m8/feeds/']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(auth.service_account_keys, scopes)
    
    # query conditions
    query = gdata.contacts.client.ContactsQuery()
    query.max_results = maxint
    
    # load & iterate over accounts
    accounts = lm_source.load() if args['--from-file'] else args['<source-accounts>']
    exclusions = lm_exclusions.load()
    
    print 'Processing accounts...\n'
    for account in accounts:
        
        print ' >> %s' % account,
        
        # prepare requestor credentials
        requestor_id = '%s@%s' % (account, domain)
        delegated_credentials = credentials.create_delegated(requestor_id)

        # authorize google datastore client
        gd_client = gdata.contacts.client.ContactsClient(domain = domain, source = 'gcontacts')
        gdata.gauth.OAuth2TokenFromCredentials(delegated_credentials).authorize(gd_client)

        try: feed = gd_client.GetContacts(q = query)
        except Exception as e: print '- Error: ', str(e); continue
        if not feed.entry: continue
        
        addresses = []
        for i, entry in enumerate(feed.entry):
            for email in entry.email:
                
                for exclusion in exclusions:
                    if exclusion in email.address: break
                else:
                    addresses.append(email.address)
                    
        lm_acc_export = ListManager(file = join(final_output_folder, '%s.txt' % account), load = False)
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
    