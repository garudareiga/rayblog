#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals


AUTHOR = u'Ray Chen'
SITENAME = u"Ray's Blog"
SITEURL = ''

TIMEZONE = 'US/Pacific'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/garudareiga'),
          ('github', 'https://github.com/garudareiga'),)

DEFAULT_PAGINATION = 5

#ARTICLE_SAVE_AS='posts/{date:%Y}/{slug}.html'
#ARTICLE_URL='posts/{date:%Y}/{slug}.html'
#YEAR_ARCHIVE_SAVE_AS='posts/{date:%Y}/index.html'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
#THEME = 'theme/bootlex'
#THEME='../pelican-themes/pelican-bootstrap3'
THEME='theme/pelican-bootstrap3'
PLUGIN_PATH='../pelican-plugins'
#PLUGINS=['sitemap']
#PLUGINS=['sitemap', 'latex']

#SITEMAP = {
#    'format': 'xml',
#    'changefreqs': {
#            'pages': 'weekly',
#    }
#}
