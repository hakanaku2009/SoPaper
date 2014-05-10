#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: job.py
# Date: Sat May 10 23:23:54 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from lib.textutil import title_beautify
from uklogger import *

class JobContext(object):
    def __init__(self, query):
        self.query = query
        self.success = False
        self.title = query
        self.search_results = []
        self.meta = {}

    def update_title(self, title):
        title = title_beautify(title)
        log_info("Using new title: {0}".format(title))
        self.title = title

    def update_meta_dict(self, meta):
        self.meta.update(meta)

class SearchResult(object):
    def __init__(self, type, url):
        self.url = url
        self.type = type
        self.searcher = None

    def __str__(self):
        return str(self.searcher) + ", " + str(self.type) + ", "+ self.url
