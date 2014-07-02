__author__ = 'Akshay'

import web
import sys
import logging
from MetaScoreFetcher import MetaScoreFetcher

DEFAULT_PORT = '8080'
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FILE_LOCATION = 'MetaScoreWebService.log'


class MetaScoreWebService(object):

    paths = ('/games(.*)', "MetaScoreFetcher")

    def __init__(self):
        self.log = logging.getLogger("MetaScoreWebService")
        self.app = web.application(self.paths, globals())

    def start_web_service(self, port=DEFAULT_PORT):
        self.log. info("Started WebService !!")
        sys.argv[1:] = [port]
        self.app.run()

if __name__ == "__main__":
    logging.basicConfig(filename=DEFAULT_LOG_FILE_LOCATION, level=DEFAULT_LOG_LEVEL)
    logging.StreamHandler()
    webService = MetaScoreWebService()
    webService.start_web_service()
