import re
from urllib import request

class URLtoText():

    def __init__(self, url_match, url_vs):
        self.url_match = url_match
        self.url_vs = url_vs
        self.html_match = request.urlopen(url_match).read().decode('utf8')
        self.html_vs = request.urlopen(url_vs).read().decode('utf8')

    def identify_players_seed_country(self):
        self.seeding_w = 0
        self.seeding_l = 0
        winner_check = re.findall(r"<strong><.*>(.*)</a></strong>", self.html_match)
        players = re.findall(r"<a href=\"player.*?>(.*?)</a>", self.html_match)
        country = re.findall(r"alt=\"(.*)\" title=\"", self.html_match)
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
        print("winner: " + str(self.winner))
        print("loser: " + str(self.loser))
        print("seeding_w: " + str(self.seeding_w))
        print("seeding_l: " + str(self.seeding_l))
        print("country_w: " + str(self.country_w))
        print("country_l:" + str(self.country_l))


    def identify_scores(self):
        scores_original = re.findall(r"<span class=\"score\">(.*)</span></td>", self.html_match)
        scores = re.findall(r"<span>(\d\d?-\d\d?)</span>", scores_original[0])
        if (re.search(r"Retired", scores_original[0])):
            scores.append("Retired")
        self.scores = scores
        print("scores: " + str(self.scores))

    def identify_duration(self):
        duration_str = re.findall(r">(\d\d?:\d\d?)<", self.html_match)
        hour = re.findall(r"(\d\d?):", duration_str[0])
        minute = re.findall(r":(\d\d?)", duration_str[0])
        self.duration_in_min = int(hour[0]) * 60 + int(minute[0])
        print("duration: " + str(self.duration_in_min))

    def identify_date(self):
        self.date = re.search(r"\"plannedtime\" align=\"right\">(.*?)</td>", self.html_match).group(1)  # to match the date in previous meetings
        print("date: " + str(self.date))

    def identify_head2head_ranking(self):
        left_points = re.search(r"<.*>.*(\d+).*<.*>.*Record.*<.*>.*(\d+).*", self.html_vs).group(1)
        right_points = re.search(r"<.*>.*(\d+).*<.*>.*Record.*<.*>.*(\d+).*", self.html_vs).group(2)

        left_ranking = re.search(r"<.+?><.+?><.+?>(\d+)<.+?><.+?>Ranking<.+?><.+?>(\d+)", self.html_vs).group(1)
        right_ranking = re.search(r"<.+?><.+?><.+?>(\d+)<.+?><.+?>Ranking<.+?><.+?>(\d+)", self.html_vs).group(2)

        left_name = re.findall(r"<.+?class=\"left\"><.+?><.+?class=\"left\"><.+?>([\w+ ]+)", self.html_vs, flags=re.DOTALL)[0][:-1]
        winner = [name.lower() for name in self.winner]

        if left_name.lower() in winner:
            self.points_w = left_points
            self.points_l = right_points

            self.ranking_w = left_ranking
            self.ranking_l = right_ranking
        else:
            self.points_w = right_points
            self.points_l = left_points

            self.ranking_w = right_ranking
            self.ranking_l = left_ranking

        print("points_w: " + self.points_w)
        print("points_l: " + self.points_l)
        print("ranking_w: " + self.ranking_w)
        print("ranking_l: " + self.ranking_l)


    def identify_last_meeting(self):
        meetings = re.findall(r"<.+?class=\"plannedtime\".+?>([\w]{3} [\d]{,2}/[\d]{,2}/[\d]{4})[ <span class=\"time\">]?([\d]{,2}:[\d]{2} [\w]{2})?<.+?><.+?><.+?>([\w+\- ]+).+?<strong><.+?>([\w+ ]+)", self.html_vs, flags=re.DOTALL)
        index = 0
        for meeting in meetings:
            if meeting[0] == self.date:
                last_meeting = meetings[index + 1]
                break;
            index += 1
        self.last_meeting = []
        self.last_meeting.append(last_meeting[0])
        if last_meeting[2][-1] == ' ':
            self.last_meeting.append(last_meeting[2][:-1])
        else:
            self.last_meeting.append(last_meeting[2])
        self.last_meeting.append(last_meeting[3][:-1])
        print("last meeting: " + str(self.last_meeting))
        # winner only show one person, but for double players one is also enough to determine which team is winner


if __name__ == "__main__":
    url_match = "https://bwf.tournamentsoftware.com/sport/match.aspx?id=F0D25C8F-6A9A-49DE-97FC-E58E3DB74CF1&match=35"
    url_vs = "https://bwf.tournamentsoftware.com/ranking/headtohead.aspx?id=209B123F-AA87-41A2-BC3E-CB57133E64CC&t1p1=89785&t2p1=54346"
    url_to_text = URLtoText(url_match, url_vs)
    url_to_text.identify_players_seed_country()
    url_to_text.identify_scores()
    url_to_text.identify_duration()
    url_to_text.identify_date()
    url_to_text.identify_head2head_ranking()
    url_to_text.identify_last_meeting()