#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
import json
import itertools
import functools


def process_feature(feature):
    feature['properties']['Name'] = filter(lambda s: s.startswith('N_MUNICIPI'), feature['properties']['Description'].split('<br>'))[0].split('=')[1].strip()
    new_doc = {
        'type': 'FeatureCollection',
        'features': [feature]
    }

    return new_doc

def process_file(filename):
    with open(filename, 'r') as doc:
        json_doc = json.loads(doc.read())

    return itertools.imap(process_feature, json_doc['features'])

def save_doc(doc, name,  basepath):
    filename = os.path.join(basepath, name +'.geojson')

    try:
        os.mkdir(basepath)
    except OSError:
        pass

    with open(filename, 'w') as f:
        f.write(json.dumps(doc))

    return filename

def get_name(doc):
    return '-'.join(doc['features'][0]['properties']['Name'].lower().split())

def process_filelist(filelist, basepath):
    doc_list = list(itertools.chain.from_iterable(itertools.imap(process_file, filelist)))
    name_list = itertools.imap(get_name, doc_list)

    save_doc_ = functools.partial(save_doc, basepath=basepath)
    map(save_doc_, doc_list, name_list)


if __name__ == '__main__':
    process_filelist(sys.argv[1:-1], sys.argv[-1])
