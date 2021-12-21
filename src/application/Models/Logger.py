# Generate loggers for any type of message.
# Ashlee

import logging


class Logger:
    def __init__(self, log_type="Generic"):
        self.log_type = log_type

    # Different levels of logs
    def info(self, msg):
        logging.info("[%s] %s" % (self.log_type, msg))

    def warn(self, msg):
        logging.warning("[%s] %s" % (self.log_type, msg))

    def error(self, msg):
        logging.info("[%s] %s" % (self.log_type, msg))

    def critical(self, msg):
        logging.info("[%s] %s" % (self.log_type, msg))
