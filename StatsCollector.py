from requests import get


# Define the class
class StatsCollector:

    # Define the address and site type
    def __init__(self, url, site_type):
        self.abs_adr = url
        self.site_type = site_type

    # Define the Sofa function
    def sofa_steal(self):
        html_soup = get(self.abs_adr).json()
        # Pull all the data about the requested league
        teams = html_soup["standingsTables"][0]["tableRows"]
        return teams

    # Define the function that will interact with Felix
    def get_league(self):
        if self.site_type.lower() == "sofa":
            return self.sofa_steal()