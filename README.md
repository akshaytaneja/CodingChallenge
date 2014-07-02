CodingChallenge
===============
Following are the instruction to run the webservice on local machine which implements

 1. A method which parse the default url and parse the html page dump to get the metascore of the top games and return the information in JSON format.
 2. A REST API for retrieving top games information.

Python Package required
------------------------
 1. python-lxml (Reference: http://lxml.de/installation.html)
 2. web.py (Reference: http://webpy.org/install)
 3. Beautifulsoup (Reference: http://www.crummy.com/software/BeautifulSoup/#Download)
 
Running WebService:
-------------------
 
 1. After installing all python dependency, execute the MetaScoreWebService.py on the command line which will start a webservice at default port 8080. 
	
	`C:\Users\Akshay\Documents\GitHub\CodingChallenge\GetMetaScoreRESTAPI> python MetaScoreWebService.py`
	`http://0.0.0.0:8080`
		
 2. Open the address "http://localhost:8080/games" on a webbrowser and it should return the JSON format for the parsed MetaScore information of games.
	(See snapshot-1.jpg for reference)
 
 3. Open the address like "http://localhost:8080/games/2014%20FIFA%20World%20Cup%20Brazil" to fetch the information for a particular game title.
	(See snapshot-2.jpg for reference)
