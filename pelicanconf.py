#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals


AUTHOR = u'Ray Chen'
SITENAME = u"Ray's Thoughts and Writings"
#SITEURL = 'http://www.raydevblog.us'

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
SOCIAL = (('linkedin', 'http://www.linkedin.com/in/leichen1983'),
          ('twitter', 'https://twitter.com/garudareiga'),
          ('github', 'https://github.com/garudareiga'),)

DEFAULT_PAGINATION = 5


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
THEME='pelican-themes/pelican-bootstrap3'
PLUGIN_PATH='pelican-plugins'
PLUGINS=['sitemap', 'latex', 'pelican_gist']

SITEMAP = {
    'format': 'xml',
#    'changefreqs': {
#            'pages': 'weekly',
#    }
}
