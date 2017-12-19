from requests import get
import time
import datetime


# Define the class
class StatsCollector:

    # Define the address and site type
    def __init__(self, url, site_type):
        self.abs_adr = url
        self.site_type = site_type

    def get_dt_games(self, game_uid):
        if self.site_type.lower() == "sofa":
            return get("https://www.sofascore.com/event/{0}/json".format(game_uid)).json()

    # Define the Sofa function
    def sofa_league(self):
        json_reader = get(self.abs_adr + "/json").json()
        # Pull all the data about the requested league
        league = json_reader["standingsTables"][0]["tableRows"]

        return league

    def sofa_games(self, unix_start, unix_end):
        addr = self.abs_adr + "/matches/week/" + str(int(unix_start)) + "/" + str(int(unix_end))
        json_reader = get(addr).json()
        # Pull all the data about the requested league

        return json_reader

    # Define the function that will interact with Felix
    def get_league(self):
        if self.site_type.lower() == "sofa":
            return self.sofa_league()

    def get_games(self, start):
        if self.site_type.lower() == "sofa":
            datetime_object = datetime.datetime.strptime(start, '%Y-%m-%d')
            unix_start = time.mktime((datetime.date(datetime_object.year, datetime_object.month, datetime_object.day)).timetuple())
            unix_end = time.mktime((datetime.datetime.now()).timetuple())

            return self.sofa_games(unix_start, unix_end)