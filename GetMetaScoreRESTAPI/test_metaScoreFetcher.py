import unittest
from MetaScoreFetcher import MetaScoreFetcher

__author__ = 'Akshay'


class TestMetaScoreFetcher(unittest.TestCase):

    def setUp(self):
        self.fetcher = MetaScoreFetcher()

    def test_fetch_meta_score(self):
        pagedump = self.fetcher.fetch_meta_score_page_dump()
        print ("HTML Page Dump: %s" % pagedump)
        self.assertIsNotNone(pagedump, "Not able to process URL")

    def test_parse_html_dump(self):
        pagedump = self.fetcher.fetch_meta_score_page_dump()
        if pagedump:
            self.fetcher.parse_html_page_dump(pagedump)
            print ("Game Information: %s" % self.fetcher.gameInformation)
            self.assertIsNotNone(self.fetcher.gameInformation, "Not able to parse page dump")
        else:
            self.fail()

    def test_search_game_information(self):
        title = self.fetcher.gameInformation.values().pop(0).get_game_title()
        title = ''.join(['/', title])
        response = self.fetcher.search_game_information(title)
        print "Response:%s" % response
        self.assertIsNotNone(response, "Not able to fetch information")

    def test_GET_without_argument(self):
        response = self.fetcher.GET()
        print "Response:%s" % response
        self.assertIsNotNone(response, "Not able to fetch information")

    def test_GET_with_argument(self):
        title = self.fetcher.gameInformation.values().pop(0).get_game_title()
        title = ''.join(['/', title])
        response = self.fetcher.GET(title)
        print "Response:%s" % response
        self.assertIsNotNone(response, "Not able to fetch information")

    def test_POST(self):
        response = self.fetcher.POST()
        self.assertEqual(response, "<html>%s</html>" % "Request Not Supported")

if __name__ == '__main__':
    unittest.main()