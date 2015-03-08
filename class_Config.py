#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
#  - Author:    desko27
#  - Email:     desko27@gmail.com
#  - Version:   2.1.0
#  - Created:   2015/01/28
#  - Updated:   2015/02/14
# ----------------------------------------------------------------------------

from iniparse import INIConfig
from iniparse.config import Undefined
from codecs import open as uopen

# ---------------------------------------------------------------------------
# functions
# ---------------------------------------------------------------------------
conf_exists = lambda e: type(e) != Undefined
conf_exists_value = lambda e, value: conf_exists(e) and e == value

# ---------------------------------------------------------------------------
# classes
# ---------------------------------------------------------------------------
class Config(INIConfig):

	def __init__(self, file): super(Config, self).__init__(uopen(file, 'r', 'utf8'))
	def get_sections(self): return [e for e in self]
	def get_values_from_section(self, section): return [self[section][e] for e in self[section]]
