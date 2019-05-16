'''
Created on May 16, 2019

@author: Zhaoyu

'''
import datetime
import logging
import os
import inspect
import sys

from app.lib.project_root_path import root_path
LOG_LEVEL = logging.DEBUG

class MiLog(object):
    """
    packaged the logging of python,
    so I can write every log with different situation
    """
    @staticmethod
    def info(msg="-"*20):
        logger = set_logger()
        logger.info(" [mipi] " + str(msg))

    @staticmethod
    def debug(msg):
        logging.debug("[mipi] " + str(msg))

    @staticmethod
    def warning(msg):
        logger = set_logger()
        logger.warning("[mipi] " + str(msg))

    @staticmethod
    def error(msg):
        logger = set_logger()
        logger.error(" [mipi] " + str(msg))

    @staticmethod
    def exception(msg="Exception"):
        logger = set_logger()
        logger.exception(msg)

    @staticmethod
    def critical(msg):
        logger = set_logger()
        logger.critical(msg)

def set_logger():
    """
    define how to write log, formatter, file, level etc.
    :return: well set logger object
    """
    DAY = datetime.datetime.now().day
    MONTH = datetime.datetime.now().month


    name = inspect.stack()
    log_caller = inspect.getmodule(name[3][0])
    """
    get the globe logger object, and clear its handler.
    """
    logger = logging.getLogger(log_caller.__name__)
    logger.handlers = []
    """
    set the rule of logger
    """
    logger.setLevel(LOG_LEVEL)

    if 'linux' in sys.platform:
        os.system("mkdir -p /home/zhaoyu/mipi/month_%s" % MONTH)
        LOG_FILE_PATH = "/home/zhaoyu/mipi/month_%s/runtime_%s.log" % (MONTH, DAY)
        f_handler = logging.FileHandler(LOG_FILE_PATH)
        logger_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(logger_format)
        logger.addHandler(f_handler)

    s_handle = logging.StreamHandler(sys.stdout)
    s_handle.setLevel(logging.INFO)
    stdout_format = logging.Formatter('%(asctime)s | %(message)s')
    s_handle.setFormatter(stdout_format)
    logger.addHandler(s_handle)

    return logger


# get_time()
