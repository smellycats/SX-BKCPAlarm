# -*- coding: utf-8 -*-
import time
import datetime
import json

import arrow
import requests

import helper
from ini_conf import MyIni


class SMSSender:
    def __init__(self):
        self.myini = MyIni()
        self.sms_conf = self.myini.get_sms()
        self.kakou_ini = {
            'host': '10.47.187.165',
            'port': 80
        }
        self.id_flag = self.sms_conf['id_flag']
        self.step = 100

        self.kakou_status = False

        # 布控车牌字典形如 {'粤LXX266': {'kkdd': '东江大桥卡口',
        # 'jgsj': <Arrow [2016-03-04T09:39:45.738000+08:00]>}}
        self.bkcp_dict = {}
        
    def __del__(self):
        del self.myini

    def get_cltxmaxid(self):
        url = 'http://%s:%s/rest_hz_kakou/index.php/%s/kakou/cltxmaxid' % (
            self.kakou_ini['host'], self.kakou_ini['port'], 'hcq')
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.kakou_status = False
            raise

    def get_cltxs(self, _id, last_id):
        url = 'http://%s:%s/rest_hz_kakou/index.php/%s/kakou/cltxs/%s/%s' % (
            self.kakou_ini['host'], self.kakou_ini['port'], 'hcq', _id, last_id)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.kakou_status = False
            raise

    def get_bkcp_by_hphm(self, hphm):
        url = u'http://%s:%s/rest_hz_kakou/index.php/%s/kakou/bkcp?q=%s' % (
            self.kakou_ini['host'], self.kakou_ini['port'], 'hcq', hphm)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.kakou_status = False
            raise

    def send_sms(self, cltx):
        bkcp = self.get_bkcp_by_hphm(cltx['hphm'])
        if bkcp['total_count'] >= 1:
            try:
                print u'BKCP: {0}, {1}'.format(cltx['hphm'], cltx['jgsj'])
                memo = ''
                if bkcp['items'][0]['memo'] != None:
                    memo = bkcp['items'][0]['memo']
                data = {
                    'mobiles': bkcp['items'][0]['mobiles'].split(','),
                    'content': u'[惠城区卡口报警]%s,%s,%s,%s.(%s)' % (
                        cltx['jgsj'], cltx['kkdd'], cltx['fxbh'], cltx['hphm'],
                        memo)
                }
                #print 'data: %s' % data
                helper.sms_post(data)
            except Exception as e:
                print (e)

    def check_is_repeat(self, hphm, kkdd, jgsj):
        """检查是否重复发送"""
        # 当前时间
        t = arrow.get(jgsj)
        # 历史记录时间
        h = self.bkcp_dict.get(hphm, None)
        try:
            # 没有历史记录
            if h is None:
                return False
            # 卡口地点相同并且绝对时间差小于120秒
            if h['kkdd'] == kkdd and abs((h['jgsj'] - t).total_seconds()) < 120:
                return True
            return False
        except Exception as e:
            raise
        finally:
            self.bkcp_dict[hphm] = {'kkdd': kkdd, 'jgsj': t}
        
    def loop_get_data(self):
        self.id_flag = self.get_cltxmaxid()['maxid'] - 100
        while 1:
            try:
                maxid = self.get_cltxmaxid()['maxid']
                if self.id_flag < maxid:
                    #print self.id_flag
                    cltx_dict = self.get_cltxs(
                        self.id_flag, self.id_flag+self.step)
                    if cltx_dict['total_count'] > 0:
                        for i in cltx_dict['items']:
                            if i['clbj'] in set(['B', 'L']):
                                #print 'bkcp:%s,%s'%(i['hphm'], i['jgsj'])
                                #self.send_sms(i)
                                if not self.check_is_repeat(
                                    i['hphm'], i['kkdd'], i['jgsj']):
                                    self.send_sms(i)
                    if self.id_flag+self.step < maxid:
                        #print 'test'
                        self.id_flag += self.step
                        #self.myini.set_sms(self.id_flag)
                    elif cltx_dict['total_count'] > 0:
                        #print 'my_id:%s' % (cltx_dict['items'][-1]['id'])
                        self.id_flag = cltx_dict['items'][-1]['id']
                        #self.myini.set_sms(self.id_flag)
                    time.sleep(0.1)
                else:
                    time.sleep(1)
            except Exception as e:
                print (e)
                time.sleep(5)

if __name__ == "__main__":
##    print 'main'
##    while 1:
##        try:
##            fd = SMSSender()
##            fd.loop_get_data()
##        except Exception as e:
##            print e
##            time.sleep(15)
    fd = SMSSender()
    fd.loop_get_data()
    del fd
    #s = SMSSender()
    #s.get_bkcp_by_hphm(u'粤LXX266')
    #del s


