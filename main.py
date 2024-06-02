import squarify
import matplotlib.pyplot as plt
import pandas as pd


class Palette:


    def __init__(self, colors: list[str], thresholds: list[int]):
        self.colors = colors
        self.thresholds = thresholds


    def get_color(self, value):
        for i, threshold in enumerate(self.thresholds[:-1]):
            if threshold < value <= self.thresholds[i+1]:
                return self.colors[i]


    def draw_palette(self):
        ...


def get_color(Palette, value):
    return Palette.get_color(value)


def add_colors(df: pd.DataFrame, colors: dict[str, Palette]) -> pd.DataFrame:
    """Adds colors to df.

    Args:
        df (pd.DataFrame). The data to be used. It should have the following
        columns:
        * name: the name of the subdivision, i.e. precinct/county/state/country.
        * total: the total amount of votes cast.
        * winner_votes: the amount of votes received by the winner.
        * winner_name: the winner's name.
        colors (dict[str, Palette]): the dict linking winner's names
        (should be compatible with df's winnter_name) and palettes.

    Returns:
        A new df, with three columns: name, total (old) and color (new).
    """
    df["winner_percent"] = (df["winner_votes"] / df["total"] * 100).round(2)
    df["palette"] = df["winner_name"].apply(lambda x: colors[x])
    df["color"] = df.apply(lambda x: get_color(x["palette"],
                                               x["winner_percent"]), axis=1)
    return df[["name", "total", "color"]]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df = pd.read_excel("example0.xlsx", header=0)
    df = add_colors(df, {"Garza": Palette(["#FFB2B2"], [40, 50])})
    print(df.to_string())
