__author__ = 'Akshay'

import re
import json
import urllib2
import logging
from bs4 import BeautifulSoup

DEFAULT_URL = "http://www.metacritic.com/game/playstation-3"
DEFAULT_HREF_HEAD = "/game/playstation-3"


class MetaScoreFetcher(object):

    def __init__(self):
        """Default Constructor"""
        self.log = logging.getLogger('MetaScoreFetcher')
        self.gameInformation = {}
        self.load_game_information()

    def GET(self, gameTitle=None):
        """HTTP GET Method invoked when user tries to access either of pages
            - "/games", return the MetaScore of all games in JSON format
            - "/games/TITLE_OF_GAME", return MetaScore
        """
        response = None
        if (gameTitle):
            self.log.info("Game Title Received: %s" % gameTitle)
            response = self.search_game_information(gameTitle)
        else:
            response = self.serialize()

        self.log.info("Response to user:%s" % response)
        return response

    def POST(self):
        """Handles the POST Request
        Currently, not implemented
        """
        return "<html>%s</html>" % "Request Not Supported"

    def add_game_information(self, info):
        """ Add the GameInformation object to dictionary and 'href' as the key
        :param info: A GameInformation Object
        :return: None
        """
        self.gameInformation[info.get_href_title()] = info

    def update_game_information(self, href, score):
        """ Update the dictionary of GameInformation object for the given parameters
        :param href: Used as a key to find the GameInformation object
        :param score: MetaScore information
        :return: None
        """
        if href in self.gameInformation:
            self.gameInformation[href].set_meta_score(score)
        else:
            self.gameInformation[href] = GameInformation({'href': href, 'MetaScore': score})

    def load_game_information(self):
        """Invoke the Fetch metascore method to load the page dump of the URl
        and update the dictionary of
        :return: None
        """
        pagedump = self.fetch_meta_score_page_dump()
        self.parse_html_page_dump(pagedump)

    def fetch_meta_score_page_dump(self):
        """Capture the DEFAULT URL webpage and return the page dump
         for further processing.
         """
        page = ""
        site = DEFAULT_URL
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, \
                  like Gecko) Chrome/23.0.1271.64 Safari/537.11',\
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
                  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',\
                  'Accept-Encoding': 'none',\
                  'Accept-Language': 'en-US,en;q=0.8',\
                  'Connection': 'keep-alive'}

        request = urllib2.Request(site, headers=header)

        try:
            page = urllib2.urlopen(request)
        except urllib2.HTTPError, error:
            self.log.error(error.fp.read())
        except urllib2.URLError, error:
            self.log.error(error)
        return page.read()

    def parse_html_page_dump(self, pageDump):
        """This method process the page information to extract and save the following game information
            - Title
            - MetaScore
            - href (common element between two find_all call.)
         """
        htmlParser = BeautifulSoup(pageDump)
        '''Parse the Title information and store it as a dictionary of GameInformation object
        with `href` as the key.
        '''
        titleInformation = htmlParser.find_all('div', {'class': "basic_stat product_title"})
        self.log.info(titleInformation)

        for info in titleInformation:
            newEntry = GameInformation()
            self.log.info(info.find("a").contents[0])
            self.log.info(info.find("a")["href"])
            newEntry.set_game_title(info.find("a").contents[0])
            newEntry.set_href_title(info.find("a")["href"])
            self.add_game_information(newEntry)

        '''Parse the MetaScore information and update the GameInformation object for the
        particular 'href'
        '''
        metaScoreInformation = htmlParser.find_all('a', {'class': "basic_stat product_score"})
        self.log.info(metaScoreInformation)
        for info in metaScoreInformation:
            self.log.debug("href: %s" %info["href"])
            self.log.debug("MetaScore: %s" %info.find("span").contents[0])
            self.update_game_information(info["href"], info.find("span").contents[0])

    def search_game_information(self, title):
        """Look up the Game information dictionary for information about a 'title'
         provided and return it's information in JSON format if present.
        """
        href = self.__convert_game_title_string_to_href_string(title.lower())
        response = {}
        if href in self.gameInformation:
            response = self.gameInformation[href].serialize()

        return json.dumps(response, indent=4, separators=(',', ':'))

    def __convert_game_title_string_to_href_string(self, title):
        """Converts the given `title` argument into href formart.

        :param title: Name of the game title received as a input to GET method
        :return: convert the argument into href string.
        """
        title = re.sub('[:]', '', title)
        return ''.join([DEFAULT_HREF_HEAD, re.sub(' ', '-', title)])

    def serialize(self):
        "Serializes this object in a JSON compatible format"

        serializedList = []
        for info in self.gameInformation.values():
            serializedList.append(info.serialize())

        return json.dumps(serializedList, indent=4, separators=(',', ':'))


class GameInformation(object):

    def __init__(self, *args, **kwargs):
        """Default constructor to store the parsed GameInformation
        """
        if ('title' in kwargs):
            self.set_game_title(kwargs.get('title'))
        else:
            self.set_game_title(None)

        if ('MetaScore' in kwargs):
            self.set_meta_score(kwargs.get('MetaScore'))
        else:
            self.set_meta_score(0)

        if ('href' in kwargs):
            self.set_href_title(kwargs.get('href'))
        else:
            self.set_href_title(None)

    def set_game_title(self, title):
        """Set the Title of the Game Information object
        :param title: Game title
        :return: None
        """
        self.gametitle = title

    def set_meta_score(self, metascore):
        """Set the Metascore of the GameInformation Object
        :param metascore: Metascore of the game
        :return: None
        """
        self.gamemetascore = metascore

    def set_href_title(self, href):
        """Set the common 'href' for a GameInformation object
        :param href:
        :return: None
        """
        self.hreftitle = href

    def get_game_title(self):
        """Get the Title of the Game Information object
        :return: Game title
        """
        return self.gametitle

    def get_meta_score(self):
        """Get the Metascore of the GameInformation Object
        :return: Metascore of the game
        """
        return self.gamemetascore

    def get_href_title(self):
        """Get the common 'href' for a GameInformation object
        :return: hreftitle
        """
        return self.hreftitle

    def serialize(self):
        "Serializes this object in a JSON compatible format"
        d = {}
        d['title'] = self.get_game_title()
        d['MetaScore'] = self.get_meta_score()
        return d


class GameInformationDecoder(json.JSONDecoder):
    "Decodes an JSON object "
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.deserialize)

    def deserialize(self, d):
        "Deserializes an object from the specified dictionary"
        return GameInformation(**d)