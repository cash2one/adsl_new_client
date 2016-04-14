# -*- coding:utf-8 -*-

from adsl2 import Adsl
import urllib, socket, logging, time
from logging import FileHandler

SERVER_URL_REPORT = 'http://adsl2.proxy.op.dajie-inc.com/host/report'
SERVER_URL_STATUS = 'http://adsl2.proxy.op.dajie-inc.com/list/status'


def report(hostname):
    data = urllib.urlencode({'host': hostname})
    ret = urllib.urlopen(SERVER_URL_REPORT, data=data).read()
    return ret


def main():
    hostname = socket.gethostname()
    try:
        while True:
            ret1 = urllib.urlopen(SERVER_URL_STATUS + '?show=' + hostname).read()
            logging.info(ret1)
            if str(ret1).strip() == 'used':
                Adsl.reconnect()
                ret2 = report(hostname=hostname)
                logging(ret2)
            else:
                time.sleep(1)
    except KeyboardInterrupt, e:
        logging.info(str(e))


if __name__ == '__main__':
    FILE_NAME = 'adsl-' + time.strftime('%Y-%m-%d', time.localtime()) + '.log'
    LOG_FILE = '/var/log/' + FILE_NAME

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s',
                        filemode='a',
                        filename=LOG_FILE)
    logger = logging.getLogger(__name__)

    main()
