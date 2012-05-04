import logging
from optparse import OptionParser
from nose.plugins.logcapture import LogCapture
from nose.tools import eq_
from ketchlip.helpers import klogger

def test_logging():
    c = LogCapture()
    parser = OptionParser()
    c.addOptions(parser, {})
    logger = klogger.get_logger("foo")
    logger = klogger.get_module_logger(__name__)
    c.start()

    logger.info("Goodbye")

    c.end()
    records = c.formatLogRecords()
    eq_("Goodbye", c.handler.buffer[0].msg)
    eq_("test.helpers.klogger_test", c.handler.buffer[0].name)
    eq_("test.helpers.klogger_test: INFO: Goodbye", records[0])
