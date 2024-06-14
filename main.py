import squarify
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


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


def make_tree_map(df: pd.DataFrame):
    labels = [i for i in df["name"]]
    sizes = [i for i in df["total"]]
    num_labels_in_legend = np.count_nonzero(np.array(sizes) / sum(sizes) < 0.02)
    if num_labels_in_legend:
        updated_labels = labels[:-num_labels_in_legend]+[""]*num_labels_in_legend
    else:
        updated_labels = labels
    ax = squarify.plot(sizes, label=updated_labels,
                  color=df["color"], norm_y=10, norm_x=10,
                  edgecolor="white", linewidth=1)
    ax.axis('off')
    ax.invert_yaxis()
    #leg = plt.legend(handles=ax.containers[0][:-num_labels_in_legend - 1:-1],
    #           labels=labels[:-num_labels_in_legend - 1:-1],
    #           handlelength=1, handleheight=1)
    #leg.get_frame().set_linewidth(0.0)
    plt.savefig("test1.svg", bbox_inches="tight")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ovp_palette = Palette(["#D0F9F9", "#ACF2F2", "#7DDDDD"], [20, 30, 40])
    fpo_palette = Palette(["#DFEEFF", "#BDD3FF", "#A5B0FF"], [20, 30, 40])
    spo_palette = Palette(["#FFE0EA", "#FFC8CD", "#FFB2B2"], [20, 30, 40])
    df = pd.read_excel("osterreich.xlsx", header=0)
    df = add_colors(df, {"FPO": fpo_palette,
                         "OVP": ovp_palette,
                         "SPO": spo_palette})
    print(df.to_string())
    ax = make_tree_map(df)
    #plt.show()
