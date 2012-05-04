#-*- coding: utf-8 -*-

import logging
from ketchlip.helpers import config

def get_logger(logger_name, log_file = "ketchlip.log"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(config.config.log_dir + log_file)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def info(msg, *args, **kvargs):
    logger.info(msg, *args, **kvargs)

def error(msg, *args, **kvargs):
    logger.error(msg, *args, **kvargs)

def exception(msg, *args):
    logger.exception(msg, *args)

def get_module_logger(module_name):
    return logging.getLogger(module_name)

logger = get_logger('ketchlip')

