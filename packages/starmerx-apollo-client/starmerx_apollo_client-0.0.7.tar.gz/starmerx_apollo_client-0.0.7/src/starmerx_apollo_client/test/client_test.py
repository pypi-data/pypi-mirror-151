# @Time    : 2022/5/14 15:19
# @Author  : chengwenxian@starmerx.com
# @Site    : 
# @Software: PyCharm
# @Project : amazon_project
# TODO: Test demo for using client
import os
import time
import unittest

APOLLO_CONFIG_URL = 'your config server url'
APOLLO_APP_ID = 'your application id'
APOLLO_ACCESS_KEY_SECRET = 'the secret for your application'


class ApolloClientCase(unittest.TestCase):

    @classmethod
    def test_client_with_logger(cls):
        """
        1. get value with default value
        2. get value in json format
        3. use customer logger
        :return:
        """

        from ..apollo_client import ApolloClient
        logger = cls.get_logger()
        a_client = ApolloClient(
            app_id=APOLLO_APP_ID, secret=APOLLO_ACCESS_KEY_SECRET, config_url=APOLLO_CONFIG_URL, logger=logger
        )
        print(a_client.get_value('BACKEND_BASE_URL'))
        print(a_client.get_value('BACKEND_BASE_URL', default_val='cwx'))
        while True:
            time.sleep(30)

    @classmethod
    def test_client_without_logger(cls):
        """
        1. get value with default value
        2. get value in json format
        :return:
        """

        from ..apollo_client import ApolloClient
        a_client = ApolloClient(
            app_id=APOLLO_APP_ID, secret=APOLLO_ACCESS_KEY_SECRET, config_url=APOLLO_CONFIG_URL
        )
        print(a_client.get_value('BACKEND_BASE_URL'))
        print(a_client.get_value('BACKEND_BASE_URL', default_val='cwx'))
        while True:
            time.sleep(30)

    @classmethod
    def get_logger(cls):
        import logging
        from logging.handlers import TimedRotatingFileHandler
        from datetime import datetime
        base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        log_dir_path = os.path.join(base_dir, 'logs/apollo')
        log_path = os.path.join(log_dir_path, '{date}.log'.format(date=datetime.now().strftime('%Y-%m-%d')))
        os.makedirs(log_dir_path, exist_ok=True)

        logger = logging.getLogger(__name__)
        fh = TimedRotatingFileHandler(filename=log_path, when='d', backupCount=3, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'))
        logger.addHandler(fh)
        print(logger.handlers)
        return logger
