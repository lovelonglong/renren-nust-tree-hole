#!usr/bin/env python
# -*- encoding: u8 -*-

import urllib2
import urllib
import cookielib


class Net(object):
    def __init__(self, save=None):
        self.save = save
        self.cookie = cookielib.LWPCookieJar(save)
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')]
        urllib2.install_opener(self.opener)

    def post(self, url, params):
        html = self.opener.open(urllib2.Request(url, urllib.urlencode(params))).read()
        return self.save_cookie(html)

    def get(self, url):
        html = self.opener.open(urllib2.Request(url)).read()
        return self.save_cookie(html)

    def save_cookie(self, html):
        if self.save is not None:
            self.cookie.save()
        return html
