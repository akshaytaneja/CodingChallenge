__author__ = 'Akshay'

import unittest
from MetaScoreWebService import MetaScoreWebService
from MetaScoreFetcher import GameInformationDecoder


class TestMetaScoreWebService(unittest.TestCase):
    def setUp(self):
        self.service = MetaScoreWebService()
        self.decoder = GameInformationDecoder()

    def test_web_service_response_status(self):
        response = self.service.app.request("/games")
        print("Requested Page: %s" % "/games")
        print ("Response; %s" % response.status)
        self.assertEqual(response.status,'200 OK')

    def test_web_service_response_data(self):
        response = self.service.app.request("/games")
        print("Requested Page: %s" % "/games")
        self.assertIsNotNone(response.data, "Unable to fetch information")
        print("Response data: %s" % response.data)

    def test_web_service_response_data_with_game_title(self):
        response = self.service.app.request("/games/2014 FIFA World Cup Brazil")
        print("Requested Page: %s" % "/games/2014%20FIFA%20World%20Cup%20Brazil")
        self.assertIsNotNone(response.data, "Unable to fetch information")
        print("Response data: %s" % response.data)

if __name__ == '__main__':
    unittest.main()