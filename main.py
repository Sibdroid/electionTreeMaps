import squarify
import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint


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


def _get_color(Palette, value):
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
    df["color"] = df.apply(lambda x: _get_color(x["palette"],
                                                x["winner_percent"]), axis=1)
    df = df[["name", "total", "color"]]
    # Sorting is necessary for the squarify
    return df.sort_values("total", ascending=False)


def make_tree_map(df: pd.DataFrame) -> plt.Axes:
    labels = [i for i in df["name"]]
    sizes = [i for i in df["total"]]
    num_labels_in_legend = 5
    ax = squarify.plot(sizes, label=labels[:-num_labels_in_legend]+[""]*num_labels_in_legend,
                  color=df["color"], norm_y=10, norm_x=10,
                  edgecolor="white", linewidth=1)
    ax.axis('off')
    ax.invert_xaxis()
    ax.set_aspect('equal')
    plt.legend(handles=ax.containers[0][:-num_labels_in_legend - 1:-1],
               labels=labels[:-num_labels_in_legend - 1:-1],
               handlelength=1, handleheight=1)
    plt.show()
    #plt.savefig("test0.svg", bbox_inches="tight")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    red_palette = Palette(["#FFF0F5", "#FFE0EA", "#FFC8CD", "#FFB2B2",
                           "#E27F7F", "#D75D5D", "#D72F30", "#C21B18",
                           "#A80000"], [i*10 for i in range(1, 11)])
    teal_palette = Palette(["#E3F7F7", "#D0F9F9", "#ACF2F2", "#7DDDDD",
                            "#51C2C2", "#2AACAC", "#009696", "#008080",
                            "#006666"], [i*10 for i in range(1, 11)])
    df = pd.read_excel("example0.xlsx", header=0)
    df = add_colors(df, {"Furman": red_palette, "Garza": teal_palette})
    ax = make_tree_map(df)
    #plt.show()
