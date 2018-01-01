from jinja2 import Environment

template_raw = """"""


class ImageCreator:
    def __init__(self, url, png):
        self._url = url
        self._png = png

    def create_png_output(self):
        pass


def create_html_output(html, args):
    print Environment().from_string(html).render(logoleft=args["logo-left"], logoright=args["logo-right"])


if __name__ == "__main__":
    # tt = TemplateTranslator(r"C:\GetBet\Matchups\matchup_template.tmpl", "C:\GetBet\Matchups\matchup_output.html")
    ic = ImageCreator("C:\GetBet\Matchups\matchup_output.html", "C:\GetBet\Matchups\matchup_output.png")

    team_logo_left = ""
    team_logo_right = ""

    params = {}
    params["logo-left"] = r"C:\GetBet\Images\England\280X280_0004_Arsenal.png"
    params["logo-right"] = r"C:\GetBet\Images\England\280X280_0011_Liverpool.png"
    params["param-0"] = {"param-value-left": "4", "param-value-left": "6", "param-name": "Broke lead", "param-type": "+"}

    create_html_output(template_raw, params)
    """
    TBD
    params["param-1"] = ["5", "5", "Scored at 0-15 min" "+"]
    params["param-2"] = ["3", "7", "Gained points at 80+ min" "+"]
    params["param-3"] = ["2", "4", "Conceded goals at 0-15 min" "-"]
    params["param-4"] = ["2", "0", "Lost points at 80+ min" "+"]

    tt.create_html_output(params)
    ic.create_png_output()
    """
