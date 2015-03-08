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

# ---------------------------------------------------------------------------
# classes
# ---------------------------------------------------------------------------
class ListManager:

    def __init__(self, list = [], file = None, load = True):
        self.list = list
        self.file = file
        if file != None and load: self.load()
        
    def load(self, file = None):
        file = self.file_check(file)
            
        # load the list from file
        self.list = []
        with uopen(file, 'r', 'utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if (len(line) > 0 and line[0] == '#') or len(line.split()) == 0:
                    continue
                items = line.split(',')
                for item in items:
                    if len(item.strip()) == 0: continue
                    item = item.strip()
                    if item != u"": self.list.append(item)
                    
        return self.list
        
    def save(self, file = None):
        file = self.file_check(file)
        
        # save the list to file
        with uopen(file, 'w', 'utf-8') as f:
            f.write(u'\r\n'.join(self.list))

        self.file = file
        
    def file_check(self, file = None):
        if file == None and self.file != None:
            file = self.file
        elif file == None:
            raise Exception('No file was specified!')
        return file
        
    def unique_elements(self):
        self.list = list(set(self.list))
    