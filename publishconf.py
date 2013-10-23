#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

#SITEURL = '.'
SITEURL = 'http://garudareiga.github.io/rayblog'
#SITEURL = 'http://www.raydevblog.us'
#RELATIVE_URLS = False
RELATIVE_URLS = True 

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

FILES_TO_COPY = (('extra/CNAME', 'CNAME'),)

# Following items are often useful when publishing

DISQUS_SITENAME = "garudareiga"
#GOOGLE_ANALYTICS = ""
