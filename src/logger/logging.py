import logging
import pandas as pd

class Logger:
    def __init__(self, log_file='app.log'):
        self.logger = logging.getLogger('Loggin_Validate_Data')
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

