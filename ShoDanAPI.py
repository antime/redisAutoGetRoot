#!/usr/bin/env python
#_*_ encoding:utf-8 _*_

import shodan

class ShoDanSearch(object):

    SHODAN_API_KEY = ''

    def __init__(self, keywords):
        self.keywords = keywords
        self.api = shodan.Shodan(self.SHODAN_API_KEY)
        self.ipList = []

    def getKeyString(self):
        print self.SHODAN_API_KEY

    def getSearchInfo(self):
        try:
            result = self.api.search(self.keywords)
            print 'Results found: %s' % result['total']
            for res in result['matches']:
                # print res['ip_str']
                self.ipList.append(res['ip_str'])
            return self.ipList
        except shodan.APIError,e:
            print 'Error: %s' % e
