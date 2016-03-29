# -*- coding: utf-8 -*-
import json

import requests


class Kakou(object):
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.city = kwargs['city']
        self.headers = {'content-type': 'application/json'}

        self.status = False

    def get_maxid(self):
        """获取最大ID值"""
        url = u'http://{0}:{1}/rest_hz_kakou/index.php/{2}/kakou/cltxmaxid'.format(
            self.host, self.port, self.city)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.status = False
            raise

    def get_cltxs(self, _id, last_id):
        """根据ID范围获取车辆信息"""
        url = u'http://{0}:{1}/rest_hz_kakou/index.php/{2}/kakou/cltxs/{3}/{4}'.format(
            self.host, self.port, self.city, _id, last_id)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.status = False
            raise

    def get_bkcp_by_hphm(self, hphm):
        """根据车牌号码获取布控信息"""
        url = u'http://{0}:{1}/rest_hz_kakou/index.php/{2}/kakou/bkcp?q={3}'.format(
            self.host, self.port, self.city, hphm)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.status = False
            raise

