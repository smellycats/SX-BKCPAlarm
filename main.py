# -*- coding: utf-8 -*-
import os
import time
import datetime
import json

import arrow
import requests

from helper_kakou2 import Kakou
from helper_sms import SMS
from ini_conf import MyIni
from my_logger import *


debug_logging(u'/home/logs/error.log')
logger = logging.getLogger('root')


class BKCPAlarm(object):
    def __init__(self):
        self.my_ini = MyIni()

        self.sms = SMS(**self.my_ini.get_sms())
        self.kakou = Kakou(**self.my_ini.get_kakou())
        #self.id_flag = self.sms_conf['id_flag']
        self.step = 1000

        # 布控车牌字典形如 {'粤LXX266': {'kkdd': '东江大桥卡口',
        # 'jgsj': <Arrow [2016-03-04T09:39:45.738000+08:00]>}}
        self.bkcp_dict = {}
        # 布控车辆信息字典
        self.bkcp_info_dict = {}
        # 城市名
        self.cityname = self.my_ini.get_kakou()['cityname']
        
    def __del__(self):
        del self.my_ini

    def send_sms(self, cltx):
        """发送短信"""
	bkcp = self.kakou.get_bkcp(cltx['hphm'])
        if bkcp is None:
	    return
        try:
            logger.info(u'BKCP: {0}, {1}'.format(cltx['hphm'], cltx['jgsj']))
            if bkcp['memo'] is None:
                bkcp['memo'] = ''
            mobiles = bkcp['mobiles']
            content = u'[{0}卡口报警]{1},{2},{3},{4}.({5})'.format(
                self.cityname, cltx['jgsj'], cltx['kkdd'], cltx['fxbh'],
                cltx['hphm'], bkcp['memo'])
            self.sms.sms_send(content, mobiles)
        except Exception as e:
            logger.error(e)

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

    def check_bkcp(self):
	"""检查布控车牌"""
        maxid = self.kakou.get_maxid()
	#print 'self.id_flag = %s' % self.id_flag
        if self.id_flag < maxid:
            kakou_info = self.kakou.get_kakou(
                self.id_flag+1, self.id_flag+self.step)
            if kakou_info['total_count'] > 0:
                for i in kakou_info['items']:
                    if i['clbj'] in set(['B', 'L']):
                        if not self.check_is_repeat(
                            i['hphm'], i['kkdd'], i['jgsj']):
                            self.send_sms(i)
            if self.id_flag+self.step < maxid:
                self.id_flag += self.step
            elif kakou_info['total_count'] > 0:
                self.id_flag = kakou_info['items'][-1]['id']
            time.sleep(0.5)
        else:
            time.sleep(0.5)

    def run(self):
	ini_flag = False
        while 1:
            try:
		if ini_flag:
		    self.check_bkcp()
		else:
		    self.id_flag = self.kakou.get_maxid()
		    ini_flag = True
            except Exception as e:
                logger.error(e)
                time.sleep(10)
            finally:
                time.sleep(1)


