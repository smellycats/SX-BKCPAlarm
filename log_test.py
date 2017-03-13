# -*- coding: utf-8 -*-
from my_logger import *


online_logging(u'logs/access.log')
logger = logging.getLogger('root')

def log_test1():
    logger.error(u'死肥仔')

if __name__ == "__main__":
    log_test1()
