from ConfigManager import ConfigManager
from StatsCollector import StatsCollector

if __name__ == "__main__":
    config = ConfigManager("Config.xml")
    config.recursive_get_xml(config.root, 0)

    for holder in config.holder:
        if holder[1] == "league":
            url = holder[2]["url"]
            print url
            collector = StatsCollector(url, "sofa")
            league = collector.get_league()

            for team in league:
                print team["position"] + ". " + team["team"]["name"] + " [" + \
                      team["totalFields"]["matchesTotal"] + "," + \
                      team["totalFields"]["winTotal"] + "," + \
                      team["totalFields"]["drawTotal"] + "," + \
                      team["totalFields"]["lossTotal"] + "," + \
                      team["totalFields"]["pointsTotal"] + "]"
