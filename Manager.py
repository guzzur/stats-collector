from ConfigManager import ConfigManager
from StatsCollector import StatsCollector
from beautifultable import BeautifulTable
from unicodedata import normalize

line_width = 80
delimeter = "=" * line_width
delimeter_minus = "-" * line_width


def print_league_table(league):
    table = BeautifulTable()
    table.column_headers = ["Pos.", "Team", "P", "W", "D", "L", "Goals", "GD", "P"]

    for t in league:
        tname = unicode_normalize(t["team"]["name"])
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
          str(unicode_normalize(game["awayTeam"]["name"]))


def print_game_goals(game):
    pass


def query_team_broke_lead(game, home_team_name, away_team_name):
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
        print delimeter_minus


def query_last_minutes_points(game, home_team_name, away_team_name):
    bLastMinutesPoints = False
    for event in game_events["incidents"]:
        if event["incidentType"] == "goal":
            if event["homeScore"] == event["awayScore"] or abs(event["homeScore"] == event["awayScore"]):
                bLastMinutesPoints = True
                if event["scoringTeam"] == 1:
                    team_name = home_team_name
                else:
                    team_name = away_team_name
                print "\t" + str(event["time"]) + "' (" + team_name + ") " + str(
                    event["homeScore"]) + " : " + str(event["awayScore"])
    if bLastMinutesPoints:
        print_game_result(game)
        print delimeter_minus


def minimum(a, b):
    if a < b:
        return a
    return b


def unicode_normalize(string):
    return normalize("NFKD", string).encode("ascii", "ignore")


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

                home_team_name = unicode_normalize(game["homeTeam"]["name"])
                away_team_name = unicode_normalize(game["awayTeam"]["name"])

                if team.lower() in home_team_name.lower() or team.lower() in away_team_name.lower():
                    query_team_broke_lead(game, home_team_name, away_team_name)

            print_heading("LAST MINUTES POINTS")
            for game in games["weekMatches"]["tournaments"][0]["events"]:
                game_events = collector.get_dt_games(str(game["id"]))

                home_team_name = unicode_normalize(game["homeTeam"]["name"])
                away_team_name = unicode_normalize(game["awayTeam"]["name"])

                if team.lower() in home_team_name.lower() or team.lower() in away_team_name.lower():
                    query_last_minutes_points(game, home_team_name, away_team_name)