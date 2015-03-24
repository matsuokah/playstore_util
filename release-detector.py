#!/usr/bin/env python

import argparse
import urllib
import sys
from HTMLParser import HTMLParser
import re
import datetime

'''
ArgumentParser Settigs.
'''
parser = argparse.ArgumentParser(description='This script is update detection for the Google play store.')
parser.add_argument('-u', '--url', type=str, required=True, nargs=1,  help="Store url.")
parser.add_argument('-d', '--date', type=str, required=True, nargs=1,  help="Publish date.")
args = parser.parse_args()

'''
Parser
'''
class AndroidVersionParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.isDatePublished = False
        self.date = ''

    '''
    ' Find software date tag.
    '''
    def handle_starttag(self, tag, attrs):
        self.isDatePublished = False 
        attrs = dict(attrs)
        if tag != 'div':
            return
        if 'itemprop' not in attrs:
            return
        if attrs['itemprop'] != 'datePublished':
            return
        self.isDatePublished = True

    '''
    ' Extraction date data.
    '''
    def handle_data(self, data):
        data = data.strip('\ \n')
        if not self.isDatePublished:
            return
        if not data:
            return
        self.date = data

'''
Main.
'''
if __name__ == "__main__":
    # Get Parser
    parser = AndroidVersionParser()
    if not parser:
        print 'none parser.'
        sys.exit(1)
    # Parse
    url = args.url[0]
    parser.feed(urllib.urlopen(url).read())
    if not parser.date:
        sys.exit(2)
    
    # Check updated date.
    split_pattern = r"\D"
    arr = re.split(split_pattern, parser.date)
    strdate = '-'.join(filter(None, arr))
    updated = datetime.datetime.strptime(strdate, '%Y-%m-%d')
    published_date = datetime.datetime.strptime(args.date[0], '%Y-%m-%d')

    if published_date != updated:
        print 'Yet!'
        print 'actual:', updated.isoformat()
        print 'expected:', published_date.isoformat()
        sys.exit(1)
    print 'release!'
