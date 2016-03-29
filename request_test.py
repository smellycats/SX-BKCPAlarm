# -*- coding: utf-8 -*-
import json

from helper_kakou import Kakou
from helper_sms import SMS
from ini_conf import MyIni


class KakouTest(object):
    def __init__(self):
        self.my_ini = MyIni()
        self.kakou = Kakou(self.my_ini.get_kakou())

    def get_maxid(self):
        print self.kakou.get_maxid()

    def get_cltxs(self):
        print self.kakou.get_cltxs(123,1235)

    def get_bkcp_by_hphm(self):
        print self.kakou.get_bkcp_by_hphm(u'粤L12345')


class SMSTest(object):
    def __init__(self):
        self.my_ini = MyIni()
        self.sms = SMS(self.my_ini.get_sms())

    def get_sms(self):
        content = u'广东实现'
        mobiles = ['15819851862']
        print self.sms.sms_send(content, mobiles)


if __name__ == '__main__':
    kt = KakouTest()
    kt.get_maxid()
    kt.get_cltxs()
    kt.get_bkcp_by_hphm()
