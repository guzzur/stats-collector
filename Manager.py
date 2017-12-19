from ConfigManager import ConfigManager
from StatsCollector import StatsCollector
from beautifultable import BeautifulTable
from unicodedata import normalize
delimeter = "-------------------------------------"


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


def team_breaked_lead(game, team):
    bBrokeLead = False
    if team in home_team_name or team in away_team_name:
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

            print_heading("LEAD BREAKS")
            for game in games["weekMatches"]["tournaments"][0]["events"]:
                game_events = collector.get_dt_games(str(game["id"]))

                home_team_name = u"".join(game["homeTeam"]["name"])
                away_team_name = u"".join(game["awayTeam"]["name"])

                team = "Sociedad"
                team_breaked_lead(game, team)

