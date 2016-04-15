# -*- coding:utf-8 -*-

from adsl2 import Adsl
import urllib, socket, logging, time, os
from logging.handlers import TimedRotatingFileHandler
import struct
import fcntl

SERVER_URL_REPORT = 'http://adsl2.proxy.op.dajie-inc.com/adsl/host/report'
SERVER_URL_STATUS = 'http://adsl2.proxy.op.dajie-inc.com/adsl/status'


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


def get_local_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
    ret = socket.inet_ntoa(inet[20:24])
    return ret


def changeupstream(ip_ppp):
    with open("tinyproxy.conf") as f:
        content = f.read()

    newcontent = content.replace("IP_PPP", ip_ppp)
    with open("/etc/tinyproxy/tinyproxy.conf", 'w') as f:
        f.write(newcontent)


def reloadservice(servicename='tinyproxy'):
    cmdstr = "service " + servicename + " reload"
    os.system(cmdstr)


def main():
    hostname = socket.gethostname()
    adsl = Adsl()
    while True:
        try:
            ret1 = urllib.urlopen(SERVER_URL_STATUS + '?show=' + hostname).read()
            logger.info('get self status:' + ret1)
            if 'used' in ret1:
                logger.info('start adsl reconnect')
                adsl.reconnect()
                ip_adsl = get_local_ip('ppp0')
                logger.info('end adsl reconnect')

                changeupstream(ip_adsl)
                logger.info('change tinyproxy upstream:' + ip_adsl)

                reloadservice('tinyproxy')
                logger.info('reload tinyproxy service')

                ret2 = report(hostname=hostname)
                logger.info('report self status:' + ret2)
            elif '404' in  ret1:
                ip_adsl = get_local_ip('ppp0')
                print 'ip_adsl: ' + ip_adsl

                changeupstream(ip_adsl)
                logger.info('change tinyproxy upstream:' + ip_adsl)

                reloadservice('tinyproxy')
                logger.info('reload tinyproxy service')

                ret2 = report(hostname=hostname)
                logger.info('report self status:' + ret2)
            else:
                ret2 = report(hostname=hostname)
                logger.info('report self status:' + ret2)
                time.sleep(1)
        except Exception, e:
            logging.info(str(e))


if __name__ == '__main__':
    LOG_FILE = '/var/log/adsl.log'
    logger = getlogger(LOG_FILE)

    main()
