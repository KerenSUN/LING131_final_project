import re
from urllib import request
#from bs4 import BeautifulSoup

class URLtoText():

    def __init__(self, url):
        self.url = url
        self.html = request.urlopen(url).read().decode('utf8')
        #self.raw = BeautifulSoup(html).get_text()

    def identify_players(self):

    def identify_score(self):

    def identify_countries(self):

    def identify_seeded_entry(self):
        
    def identify_head2head(self):
        left_points = re.search(r"<.*>.*(\d+).*<.*>.*Record.*<.*>.*(\d+).*", self.html).group(1)
        right_points = re.search(r"<.*>.*(\d+).*<.*>.*Record.*<.*>.*(\d+).*", self.html).group(2)

    def identify_world_ranking(self):
        left_ranking = re.search(r"<.+?><.+?><.+?>(\d+)<.+?><.+?>Ranking<.+?><.+?>(\d+)", self.html).group(1)
        right_ranking = re.search(r"<.+?><.+?><.+?>(\d+)<.+?><.+?>Ranking<.+?><.+?>(\d+)", self.html).group(2)

    def identify_last_meeting(self):
        last_meeting = re.findall(r"<.+?class=\"plannedtime\".+?>([\w]{3} [\d]{,2}/[\d]{,2}/[\d]{4})[ <span class=\"time\">]?([\d]{,2}:[\d]{2} [\w]{2})?<.+?><.+?><.+?>([\w+ ]+).+?<strong><.+?>([\w+ ]+)", self.html, flags=re.DOTALL)[1]
        # winner only show one person, but for double players one is also enough to determine

    def text_generator(self):

        def players_generator(self):

        def verb_generator(self):
        
