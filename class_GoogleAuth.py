#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
#  - Author:    desko27
#  - Email:     desko27@gmail.com
#  - Version:   1.0.2
#  - Created:   2015/02/05
#  - Updated:   2015/03/08
# ----------------------------------------------------------------------------

from os.path import join
from codecs import open as uopen
from gdata.gauth import TwoLeggedOAuthHmacToken

# ---------------------------------------------------------------------------
# classes
# ---------------------------------------------------------------------------
class GoogleAuth:

    def __init__(self, consumer_key, consumer_secret, username = None):
        self.consumer_key = str(consumer_key)
        self.consumer_secret = str(consumer_secret)
        self.username = str(username)
        
    def username_check(self, username = None):
        if username == None and self.username != None:
            username = self.username
        elif username == None:
            raise Exception('No username was specified!')
        return str(username)
        
    def get_token(self, username = None):
        username = self.username_check(username)
        
        # generate the two legged oauth token
        requestor_id = username + '@' + self.consumer_key
        two_legged_oauth_token = TwoLeggedOAuthHmacToken(self.consumer_key, self.consumer_secret, requestor_id)
        
        return two_legged_oauth_token
    