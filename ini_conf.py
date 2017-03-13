#-*- encoding: utf-8 -*-
import os
import ConfigParser


class MyIni(object):
    def __init__(self, confpath = 'my_ini.conf'):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(confpath)

    def __del__(self):
        del self.cf

    def get_kakou(self):
        conf = {}
        section = 'KAKOU'
        conf['host'] = self.cf.get(section, 'host')
        conf['port'] = self.cf.getint(section, 'port')
	conf['username'] = self.cf.get(section, 'username')
	conf['password'] = self.cf.get(section, 'password')
	conf['city'] = self.cf.get(section, 'city')
	conf['cityname'] = self.cf.get(section, 'cityname').decode('gbk', 'ignore')
        return conf

    def get_sms(self):
        conf = {}
        section = 'SMS'
        conf['host'] = self.cf.get(section, 'host')
        conf['port'] = self.cf.getint(section, 'port')
        conf['user'] = self.cf.get(section, 'user')
        conf['pwd']  = self.cf.get(section, 'pwd')
        return conf

    def get_mobiles(self):
        conf = {}
        section = 'MOBILES'
        conf['number'] = self.cf.get(section, 'number')
        return conf



