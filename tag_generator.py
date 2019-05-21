#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
tag_generator.py

Copyright 2017 Long Qian
Contact: lqian8@jhu.edu

This script creates tags for your Jekyll blog hosted by Github page.
No plugins required.
'''

import glob
import os
import sys

post_dir = '_posts/'
drafts_dir = '_drafts/'
tag_dir = 'tag/'

filenames = glob.glob(post_dir + '*md')
if len(sys.argv) > 1 and sys.argv[1] == '--drafts':
    print('Generating tags for drafts too')
    filenames.extend(glob.glob(drafts_dir + '*md'))

total_tags = []
for filename in filenames:
    f = open(filename, 'r', encoding='utf8')
    crawl = False
    for line in f:
        if crawl:
            current_tags = line.strip().split()
            if current_tags[0] == 'tags:':
                total_tags.extend(current_tags[1:])
                crawl = False
                break
        if line.strip() == '---':
            if not crawl:
                crawl = True
            else:
                crawl = False
                break
    f.close()
total_tags = set(total_tags)

old_tags = glob.glob(tag_dir + '*.md')
for tag in old_tags:
    os.remove(tag)
    
if not os.path.exists(tag_dir):
    os.makedirs(tag_dir)

for tag in total_tags:
    tag_filename = tag_dir + tag + '.md'
    f = open(tag_filename, 'a')
    write_str = '---\nlayout: tagpage\ntitle: \"Tag: ' + tag + '\"\ntag: ' + tag + '\rlang: en\nref: ' + tag + '\nrobots: noindex\n---\n'
    f.write(write_str)
    f.close()

    tag_filename = tag_dir + tag + '-he.md'
    f = open(tag_filename, 'a', encoding="utf-8")
    write_str = '---\nlayout: tagpage-he\ntitle: \"תגית: ' + tag + '\"\ntag: ' + tag + '\rlang: he\nref: ' + tag + '\nrobots: noindex\n---\n'
    f.write(write_str)
    f.close()
print("Tags generated, count", total_tags.__len__())
