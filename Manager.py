from ConfigManager import ConfigManager
from StatsCollector import StatsCollector


def print_league_table(league):
    print "#) Team [G, W, D, L, P]"
    for team in league:
        print team["position"] + ". " + team["team"]["name"] + " [" + \
              team["totalFields"]["matchesTotal"] + "," + \
              team["totalFields"]["winTotal"] + "," + \
              team["totalFields"]["drawTotal"] + "," + \
              team["totalFields"]["lossTotal"] + "," + \
              team["totalFields"]["pointsTotal"] + "]"


def print_game_result(game):
    print str(game["id"]) + " " + game["homeTeam"]["name"] + " " + \
          str(game["homeScore"]["current"]) + " : " + \
          str(game["awayScore"]["current"]) + " " + \
          str(game["awayTeam"]["name"])


def print_game_goals(game):
    pass


def team_breaked_lead(game, home_or_away):
    pass


def minimum(a, b):
    if a < b:
        return a
    return b


if __name__ == "__main__":
    config = ConfigManager("Config.xml")
    config.recursive_get_xml(config.root, 0)

    for holder in config.holder:
        if holder[1] == "league":
            url = holder[2]["url"]
            print url
            collector = StatsCollector(url, "sofa")

            league = collector.get_league()
            print_league_table(league)

            league_start_time = holder[2]["started"]
            games = collector.get_games(league_start_time)

            for game in games["weekMatches"]["tournaments"][0]["events"]:
                bBrokeLead = False
                game_events = collector.get_dt_games(str(game["id"]))

                home_goals = {}
                away_goals = {}

                home_team_name = u"".join(game["homeTeam"]["name"])
                away_team_name = u"".join(game["awayTeam"]["name"])

                prev_home_goals_count = -1
                prev_away_goals_count = -1

                curr_home_goals_count = -1
                curr_away_goals_count = -1

                for event in game_events["incidents"]:
                    if event["incidentType"] == "goal":
                        curr_home_goals_count = event["homeScore"]
                        curr_away_goals_count = event["awayScore"]

                        team = "Sociedad"
                        if event["homeScore"] == event["awayScore"] and (team in home_team_name or team in away_team_name):
                            bBrokeLead = True
                            if event["scoringTeam"] == 1:
                                print "\t" + str(event["time"]) + "' (" + home_team_name + ") " + str(event["homeScore"]) + " : " + str(event["awayScore"])
                            else:
                                print "\t" + str(event["time"]) + "' (" + away_team_name + ") " + str(event["homeScore"]) + " : " + str(event["awayScore"])

                        if event["scoringTeam"] == 1:
                            home_goals[str(event["time"])] = str(event["incidentClass"])
                        else:
                            away_goals[str(event["time"])] = str(event["incidentClass"])

                if bBrokeLead:
                    print_game_result(game)
                    print ""
