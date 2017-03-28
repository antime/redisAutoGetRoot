#!/usr/bin/env python
#_*_ encoding: utf-8 _*_

import zoomeye
from Config import zoomeyeLoginInfo

class ZoomeyeAPI(object):

    def __init__(self, keyword):
        self.__zoom = zoomeye.ZoomEye(zoomeyeLoginInfo.username, zoomeyeLoginInfo.password)
        self.__login = self.__zoom.login()
        self.keyword = keyword

    def getLogin(self):
        return self.__login

    def getSearchInfo(self, content, page=0):
        data = self.__zoom.dork_search(dork=content, page=page, resource='host')
        return data

    def getHostInfo(self):
        ips = []
        for p in xrange(50):
            search_data = self.getSearchInfo(content=self.keyword, page=p)
            for sd in search_data: ips.append(sd['ip'])
        return list(set(ips))
