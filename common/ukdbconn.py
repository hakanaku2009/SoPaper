#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: ukdbconn.py
# $Date: Sun May 11 13:47:05 2014 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""database connections"""

import ukconfig
from uklogger import *

try:
    from pymongo import MongoClient
except ImportError:
    from pymongo import Connection as MongoClient
from pymongo.errors import DuplicateKeyError
from bson.binary import Binary
from ukutil import pdf_compress
from lib.textutil import title_beautify, parse_file_size

_db = None

def get_mongo(coll_name=None):
    global _db
    if _db is None:
        _db = MongoClient(*ukconfig.mongo_conn)[ukconfig.mongo_db]

    if coll_name is None:
        return _db
    return _db[coll_name]

def new_paper(ctx):
    data = pdf_compress(ctx.data)
    pid = global_counter('paper')
    log_info("Add new paper: {0}, size={1}, pid={2}".format(
        ctx.title, parse_file_size(len(data)), pid))
    doc = {
        '_id': pid,
        'pdf': Binary(data),
        'title': ctx.title.lower(),
        'view_cnt': 1,
        'download_cnt': 0
    }
    doc.update(ctx.meta)

    db = get_mongo('paper')
    db.ensure_index('title')
    db.insert(doc)
    return pid

def update_meta(pid, meta):
    db = get_mongo('paper')
    db.update({'_id': pid}, {'$set': meta})

def update_view_cnt(pid):
    db = get_mongo('paper')
    db.update({'_id': pid}, {'$inc': {'view_cnt': 1}})


def global_counter(name, delta=1):
    """atomically change a global int64 counter and return the newest value;
    starting from 1
    mongo document structure:
    {
        _id: counter name
        val: current value
    }"""
    coll_name = 'global_counter'
    db = get_mongo()
    rst = db.command('findAndModify', coll_name,
                     query={'_id': name},
                     update={'$inc': {'val': delta}},
                     new=True)
    if rst['value']:
        return rst['value']['val']
    try:
        val = long(1)
        db[coll_name].insert({'_id': name, 'val': val})
        return val
    except DuplicateKeyError:
        return global_counter(name, delta)