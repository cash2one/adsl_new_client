# -*- coding:utf-8 -*-

from adsl2 import Adsl
import urllib, socket, logging, time, os
from logging.handlers import TimedRotatingFileHandler

SERVER_URL_REPORT = 'http://adsl2.proxy.op.dajie-inc.com/host/report'
SERVER_URL_STATUS = 'http://adsl2.proxy.op.dajie-inc.com/list/status'


def getlogger(logfile='./log'):
    log_path = os.path.dirname(logfile)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = TimedRotatingFileHandler(logfile, 'd')
    formatter = logging.Formatter('[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def report(hostname):
    data = urllib.urlencode({'host': hostname})
    ret = urllib.urlopen(SERVER_URL_REPORT, data=data).read()
    return ret


def main():
    hostname = socket.gethostname()
    try:
        while True:
            ret1 = urllib.urlopen(SERVER_URL_STATUS + '?show=' + hostname).read()
            logger.info(ret1)
            if str(ret1).strip() == 'used':
                Adsl.reconnect()
                ret2 = report(hostname=hostname)
                logger.info(ret2)
            else:
                time.sleep(1)
    except KeyboardInterrupt, e:
        logging.info(str(e))


if __name__ == '__main__':
    LOG_FILE = '/var/log/adsl.log'
    logger = getlogger(LOG_FILE)

    main()
