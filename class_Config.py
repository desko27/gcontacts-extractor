#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
#  - Author:    desko27
#  - Email:     desko27@gmail.com
#  - Version:   2.0.0
#  - Created:   2015/01/28
#  - Updated:   2015/02/06
# ----------------------------------------------------------------------------

from iniparse import INIConfig
from iniparse.config import Undefined
from codecs import open as uopen

# ---------------------------------------------------------------------------
# functions
# ---------------------------------------------------------------------------
conf_exists = lambda e: type(e) != Undefined

# ---------------------------------------------------------------------------
# classes
# ---------------------------------------------------------------------------
class Config(INIConfig):

	def __init__(self, file): super(Config, self).__init__(uopen(file, 'r', 'utf8'))
	def get_sections(self): return [e for e in self]
	def get_values_from_section(self, section): return [self[section][e] for e in self[section]]
