import re
from urllib import request
#from bs4 import BeautifulSoup

class URLtoText():

    def __init__(self, url):
        self.url = url
        self.html = request.urlopen(url).read().decode('utf8')
        #self.raw = BeautifulSoup(html).get_text()

    def identify_players_seed_country(self):
        self.seeding_w = 0
        self.seeding_l = 0
        winner_check = re.findall(r"<strong><.*>(.*)</a></strong>", self.html)
        players = re.findall(r"<a href=\"player.*?>(.*?)</a>", self.html)
        country = re.findall(r"alt=\"(.*)\" title=\"", self.html)
        if (len(winner_check) == 1):  # singles
            if (winner_check[0] == players[0]):  # winner in first element of the list
                seeding_1 = players[0][-2]
                if (seeding_1.isdigit()):
                    self.winner = [players[0][:-4]]
                    self.seeding_w = seeding_1
                else:
                    self.winner = [players[0]]

                seeding_2 = players[1][-2]
                if (seeding_2.isdigit()):
                    self.loser = [players[1][:-4]]
                    self.seeding_l = seeding_2
                else:
                    self.loser = [players[1]]
                self.country_w = country[0]
                self.country_l = country[1]

            else:  # winner in second position
                seeding_1 = players[1][-2]
                if (seeding_1.isdigit()):
                    self.winner = [players[1][:-4]]
                    self.seeding_w = seeding_1
                else:
                    self.winner = [players[1]]

                seeding_2 = players[0][-2]
                if (seeding_2.isdigit()):
                    self.loser = [players[0][:-4]]
                    self.seeding_l = seeding_2
                else:
                    self.loser = [players[0]]
                self.country_w = country[1]
                self.country_l = country[0]

        else:  # doubles
            if (winner_check[0] == players[0]):  # winner in first element of the list
                seeding_1 = players[0][-2]
                if (seeding_1.isdigit()):
                    self.winner = [players[0][:-4], players[1]]
                    self.seeding_w = seeding_1
                else:
                    self.winner = [players[0], players[1]]

                seeding_2 = players[2][-2]
                if (seeding_2.isdigit()):
                    self.loser = [players[2][:-4], players[3]]
                    self.seeding_l = seeding_2
                else:
                    self.loser = [players[2], players[3]]
                self.country_w = country[0]
                self.country_l = country[2]

            else:  # winner in second position
                seeding_1 = players[2][-2]
                if (seeding_1.isdigit()):
                    self.winner = [players[2][:-4], players[3]]
                    self.seeding_w = seeding_1
                else:
                    self.winner = [players[2], players[3]]

                seeding_2 = players[0][-2]
                if (seeding_2.isdigit()):
                    self.loser = [players[0][:-4], players[1]]
                    self.seeding_l = seeding_2
                else:
                    self.loser = [players[0], players[1]]
                self.country_w = country[2]
                self.country_l = country[0]

    def identify_score(self):
        scores_original = re.findall(r"<span class=\"score\">(.*)</span></td>", self.html)
        scores = re.findall(r"<span>(\d\d?-\d\d?)</span>", scores_original[0])
        if (re.search(r"Retired", scores_original[0])):
            scores.append("Retired")
        self.scores = scores

    def identify_duration(self):
        duration_str = re.findall(r">(\d\d?:\d\d?)<", self.html)
        hour = re.findall(r"(\d\d?):", duration_str[0])
        minute = re.findall(r":(\d\d?)", duration_str[0])
        self.duration_in_min = int(hour[0]) * 60 + int(minute[0])

    def identify_date(self):
        self.date = re.findall(r"\"plannedtime\" align=\"right\">(.*?)</td>", html_content)
        
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
        
