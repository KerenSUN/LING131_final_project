import re
from urllib import request
import URLtoText
import generator



def get_url(num):
    infile = open("tournaments.txt", 'r')
    line = infile.readlines()
    tournament =line[num-1].split()
    tournament_url = tournament[-1]
    infile.close()
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
    all_vs = re.findall(r"<td><a href=\"\.\.(.*?)\"", html)
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
    user_input1 = int(input("Choose among the 15 tournaments of 2018 by entering the index number (enter a number from 1 to 15): "))
    #input = sys.argv
    tournament_url = get_url(user_input1)
    #read_url(tournament_url)
    print("\n1)semi-final\n2)final\n")
    user_input2 = int(input("Choose a match day to see the reports by entering index number (enter a number from 1 to 2): "))

    infile = open("tournaments.txt", 'r')
    line = infile.readlines()
    tournament = line[user_input1 - 1].split()
    tournament_name = ' '.join(tournament[:-1])
    infile.close()
    if(user_input2 == 1):
        print("\n[Brief reports of " + tournament_name + " on semi-final day]\n")
    else:
        print("\n[Brief reports of " + tournament_name + " on final day]\n")

    match_day_url = generate_match_day_url(tournament_url, user_input2)
    #read_url(match_day_url)
    match_url_lst = generate_match_url(match_day_url)
    # print(match_url_lst)
    vs_url_lst = generate_vs_url(match_day_url)
    # print(vs_url_lst)


    for url1, url2 in zip(match_url_lst, vs_url_lst):
        url_to_text = URLtoText.URLtoText(url1, url2)
        url_to_text.identify_players_seed_country()
        url_to_text.identify_scores()
        url_to_text.identify_duration()
        url_to_text.identify_date()
        url_to_text.identify_head2head_ranking()
        url_to_text.identify_last_meeting()

        output_file = open("player_lexicon.txt", "w")
        if (len(url_to_text.winner) == 2):
            output_file.write(url_to_text.winner[0] + ", " + url_to_text.winner[1] + " NW\n")
            output_file.write(url_to_text.loser[0] + ", " + url_to_text.loser[1] + " NL\n")
        else:
            output_file.write(url_to_text.winner[0] + " NW\n")
            output_file.write(url_to_text.loser[0] + " NL\n")

        output_file.write(url_to_text.country_w + " NCW\n")
        output_file.write(url_to_text.country_l + " NCL\n")

        if (url_to_text.seeding_w != 0):
            output_file.write("No." + str(url_to_text.seeding_w) + " seed AW\n")
        if (url_to_text.seeding_l != 0):
            output_file.write("No." + str(url_to_text.seeding_l) + " seed AL\n")

        output_file.write("world ranking No." + url_to_text.ranking_w + " AW\n")
        output_file.write("world ranking No." + url_to_text.ranking_l + " AL\n")

        score_rec = ""
        for score in url_to_text.scores:
            score_rec += (score + ", ")
        output_file.write(score_rec[:-2] + " SCORE\n")

        output_file.write("in " + str(url_to_text.duration_in_min) + " minutes DURATION\n")

        if len(url_to_text.last_meeting) > 0:
            output_file.write(url_to_text.last_meeting[0] + ", " + url_to_text.last_meeting[1] + " LASTM\n")
        else:
            output_file.write("no record LASTM\n")

        output_file.write(str(url_to_text.head2head_w) + ": " + str(url_to_text.head2head_l) + " H2H\n")

        output_file.close()

        grammar = generator.load_grammar('rules.txt')
        template = generator.make_template(grammar, "S", [])
        # print(template)
        lexicon = generator.load_lexicon("lexicon.txt", "player_lexicon.txt")
        print(generator.make_sentence(template, lexicon))
