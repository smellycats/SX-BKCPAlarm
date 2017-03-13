# -*- coding: utf-8 -*-
import json

import requests
from requests.auth import HTTPBasicAuth


class Kakou(object):
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.username = kwargs['username']
        self.password = kwargs['password']
        
        self.headers = {'content-type': 'application/json'}

	self.status = False

    def get_kakou_count(self, st, et, kkdd, fxbh):
        """根据时间,地点,方向获取车流量"""
        url = 'http://%s:%s/stat?q={"st":"%s","et":"%s","kkbh":"%s","fxbh":"%s"}' % (
            self.host, self.port, st, et, kkdd, fxbh)
        try:
            r = requests.get(url, headers=self.headers,
			     auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                return json.loads(r.text)['count']
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
	    self.status = False
            raise

    def get_kkdd(self, kkdd_id):
        """获取卡口地点"""
        url = 'http://{0}:{1}/kkdd/{2}'.format(
            self.host, self.port, kkdd_id)
        try:
            r = requests.get(url, headers=self.headers,
		 	     auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                return json.loads(r.text)['items']
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
	    self.status = False
            raise

    def get_kakou(self, first_id, last_id):
	"""根据ID范围获取卡口信息"""
        url = 'http://{0}:{1}/kakou/{2}/{3}'.format(
            self.host, self.port, first_id, last_id)
        try:
            r = requests.get(url, headers=self.headers,
			     auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_maxid(self):
        """获取cltx表最大id值"""
        url = 'http://{0}:{1}/maxid'.format(self.host, self.port)
        try:
            r = requests.get(url, headers=self.headers,
			     auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                return json.loads(r.text)['maxid']
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_bkcp(self, hphm=None):
        """获取布控车辆信息"""
        url = 'http://{0}:{1}/bkcp'.format(self.host, self.port)
	if hphm is not None:
	    url += '/{0}'.format(hphm)
        try:
            r = requests.get(url, headers=self.headers,
			     auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
	    self.status = False
            raise

