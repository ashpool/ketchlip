import logging

logger = logging.getLogger('ketchlip')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('../ketchlip.log')
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