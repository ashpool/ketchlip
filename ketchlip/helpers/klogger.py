#-*- coding: utf-8 -*-

import logging
from ketchlip.helpers import config

logger = logging.getLogger('ketchlip')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(config.config.log_dir + "ketchlip.log")
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


def info(msg, *args, **kvargs):
    logger.info(msg, *args, **kvargs)

def error(msg, *args, **kvargs):
    logger.error(msg, *args, **kvargs)

def exception(msg, *args):
    logger.exception(msg, *args)