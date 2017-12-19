from ConfigManager import ConfigManager
from StatsCollector import StatsCollector
<<<<<<< HEAD
import unicodedata

delimeter = "-" * 82
=======
from beautifultable import BeautifulTable
from unicodedata import normalize
delimeter = "-------------------------------------"
>>>>>>> ea20215c94f54e188d2422371b66c6e52e46bb55


def print_league_table(league):
    table = BeautifulTable()
    table.column_headers = ["Pos.", "Team", "P", "W", "D", "L", "Goals", "GD", "P"]

    for t in league:
        tname = normalize("NFKD", t["team"]["name"]).encode("ascii", "ignore")
        table.append_row([t["position"], tname, t["totalFields"]["matchesTotal"],
                          t["totalFields"]["winTotal"], t["totalFields"]["drawTotal"],
                          t["totalFields"]["lossTotal"],
                          t["totalFields"]["goalsTotal"], t["totalFields"]["goalDiffTotal"],
                          t["totalFields"]["pointsTotal"]])
    print(table)


def print_game_result(game):
    print str(game["id"]) + " " + game["homeTeam"]["name"] + " " + \
          str(game["homeScore"]["current"]) + " : " + \
          str(game["awayScore"]["current"]) + " " + \
          str(game["awayTeam"]["name"])


def print_game_goals(game):
    pass


def team_broke_lead(game, home_team_name, away_team_name):
    bBrokeLead = False
    for event in game_events["incidents"]:
        if event["incidentType"] == "goal":
            if event["homeScore"] == event["awayScore"]:
                bBrokeLead = True
                if event["scoringTeam"] == 1:
                    team_name = home_team_name
                else:
                    team_name = away_team_name
                print "\t" + str(event["time"]) + "' (" + team_name + ") " + str(
                    event["homeScore"]) + " : " + str(event["awayScore"])
    if bBrokeLead:
        print_game_result(game)
        print delimeter


def minimum(a, b):
    if a < b:
        return a
    return b

def print_heading(heading):
    print delimeter
    print heading
    print delimeter


if __name__ == "__main__":
    config = ConfigManager("Config.xml")
    config.recursive_get_xml(config.root, 0)

    for holder in config.holder:
        if holder[1] == "league":
            url = holder[2]["url"]
            collector = StatsCollector(url, "sofa")

            league = collector.get_league()

            print_heading("LEAGUE TABLE")
            print_league_table(league)

            league_start_time = holder[2]["started"]
            games = collector.get_games(league_start_time)

            team = "Real Sociedad"
            print_heading("DETAILED DESCRIPTION: " + team.upper())
            print_heading("LEAD BREAKS")

            for game in games["weekMatches"]["tournaments"][0]["events"]:
                game_events = collector.get_dt_games(str(game["id"]))

                home_team_name = unicodedata.normalize('NFKD', game["homeTeam"]["name"]).encode('ascii','ignore')
                away_team_name = unicodedata.normalize('NFKD', game["awayTeam"]["name"]).encode('ascii','ignore')

                if team.lower() in home_team_name.lower() or team.lower() in away_team_name.lower():
                    #team_broke_lead(game, home_team_name, away_team_name)

                    bBrokeLead = False
                    for event in game_events["incidents"]:
                        if event["incidentType"] == "goal":
                            if event["homeScore"] == event["awayScore"]:
                                bBrokeLead = True
                                if event["scoringTeam"] == 1:
                                    team_name = home_team_name
                                else:
                                    team_name = away_team_name
                                print "\t" + str(event["time"]) + "' (" + team_name + ") " + str(
                                    event["homeScore"]) + " : " + str(event["awayScore"])
                    if bBrokeLead:
                        print_game_result(game)
                        print delimeter

