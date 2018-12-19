import re
from urllib import request
import sys





def get_url(num):
    infile = open("tournaments.txt", 'r')
    line = infile.readlines()
    tournament =line[num-1].split()
    tournament_url = tournament[-1]
    return tournament_url

def read_url(url):
    html = request.urlopen(url).read().decode('utf8')
    print(html)

def generate_match_day_url(tournament_url, day):
    html = request.urlopen(tournament_url).read().decode('utf8')
    all_dates = re.findall(r"&amp;d=(.*?)\">", html)
    if(day == 1):
        date = all_dates[-2]
    else:
        date = all_dates[-1]
    match_day_url = tournament_url.replace("tournament.aspx","matches.aspx") + "&d=" + date
    return match_day_url

def generate_players(match_day_url):
    html = request.urlopen(match_day_url).read().decode('utf8')
    players = re.findall(r"<a href=\"player.*?>(.*?)</a>", html)
    print(players)

def generate_match_url(match_day_url):
    match_url_lst = []
    html = request.urlopen(match_day_url).read().decode('utf8')
    all_matches = re.findall(r"match=(.*?)\"", html)
    for item in all_matches:
        match_url = tournament_url.replace("tournament.aspx","match.aspx") + "&match=" + item
        match_url_lst.append(match_url)
    return match_url_lst

def generate_vs_url(match_day_url):
    vs_url_lst = []
    html = request.urlopen(match_day_url).read().decode('utf8')
    all_vs = re.findall(r"<a href=\"\.\.(.*?)\"", html)
    for item in all_vs:
        vs_url = "https://bwf.tournamentsoftware.com" + item
        vs_url_lst.append(vs_url)
    return vs_url_lst




if __name__ == '__main__':
    print("1) PERODUA Malaysia Masters 2018\n"
          "2) DAIHATSU Indonesia Masters 2018\n"
          "3) YONEX-SUNRISE DR. AKHILESH DAS GUPTA India Open 2018\n"
          "4) YONEX All England Open 2018\n"
          "5) CELCOM AXIATA Malaysia Open 2018\n"
          "6) BLIBLI Indonesia Open 2018\n"
          "7) TOYOTA Thailand Open 2018\n"
          "8) Singapore Open 2018\n"
          "9) DAIHATSU YONEX Japan Open 2018\n"
          "10) VICTOR China Open 2018\n"
          "11) VICTOR Korea Open 2018\n"
          "12) DANISA Denmark Open 2018\n"
          "13) YONEX French Open 2018\n"
          "14) Fuzhou China Open 2018\n"
          "15) YONEX-SUNRISE Hong Kong Open 2018\n")
    user_input1 = int(input("Choose among the 15 tournaments of 2018 by entering the index number: "))
    #input = sys.argv
    tournament_url = get_url(user_input1)
    #read_url(tournament_url)
    print("\n1)semi-final\n2)final\n")
    user_input2 = int(input("Choose a match day to see the reports by entering index number: "))

    match_day_url = generate_match_day_url(tournament_url, user_input2)
    #read_url(match_day_url)
    match_url_lst = generate_match_url(match_day_url)
    print(match_url_lst)
    vs_url_lst = generate_vs_url(match_day_url)
    print(vs_url_lst)