import typing
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
from matplotlib import pyplot as plt

def confusion_matrix(x: np.ndarray, y: np.ndarray) -> pd.DataFrame:
    r"""
    Reimplemented this because sklearn.metrics.confusion_matrix
    does not provide row names and column names.
    """
    x, x_c = encode_integer(x)
    y, y_c = encode_integer(y)
    unique_x, unique_y = np.unique(x), np.unique(y)
    cm = np.empty((len(unique_x), len(unique_y)), dtype=np.int)
    for i in unique_x:
        for j in unique_y:
            cm[i, j] = np.sum((x == i) & (y == j))
    return pd.DataFrame(data=cm, index=x_c, columns=y_c)


# Avoid sklearn warning
def encode_integer(
        label: typing.List[typing.Any], sort: bool = False
) -> typing.Tuple[np.ndarray, np.ndarray]:
    label = np.array(label).ravel()
    classes = np.unique(label)
    if sort:
        classes.sort()
    mapping = {v: i for i, v in enumerate(classes)}
    return np.array([mapping[v] for v in label]), classes


def sankey(
        query: np.ndarray, ref: np.ndarray, title: str = "Sankey",
        width: int = 950, height: int = 772, tint_cutoff: int = 1,
        font: str = "Arial", font_size: float = 10.0,save_path:str = "./Sankey.png",
        export_plot: bool = False
) -> dict:  # pragma: no cover
    r"""
    Make a sankey diagram of query-reference mapping (only works in
    ipython notebooks).

    Parameters
    ----------
    query
        1-dimensional array of query annotation.
    ref
        1-dimensional array of BLAST prediction based on reference database.
    title
        Diagram title.
    width
        Graph width.
    height
        Graph height.
    tint_cutoff
        Cutoff below which sankey flows are shown in a tinter color.
    font
        Font family used for the plot.
    font_size
        Font size for the plot.
    suppress_plot
        Whether to suppress plotting and only return the figure dict.

    Returns
    -------
    fig
        Figure object fed to `iplot` of the `plotly` module to produce the plot.
    """
    cf = confusion_matrix(query, ref)
    cf["query"] = cf.index.values
    cf = cf.melt(
        id_vars=["query"], var_name="reference", value_name="count"
    ).sort_values(by="count")
    query_i, query_c = encode_integer(cf["query"])
    ref_i, ref_c = encode_integer(cf["reference"])
    fig_go = go.Figure(data=[go.Sankey(
       node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color="black",
                width=0.5
            ),
            label=np.concatenate([
                query_c, ref_c
            ], axis=0),
            color=["#E64B35"] * len(query_c) +
            ["#4EBBD5"] * len(ref_c)
        ),
        link=dict(
            source=query_i.tolist(),
            target=(
                ref_i + len(query_c)
            ).tolist(),
            value=cf["count"].tolist(),
            color=np.vectorize(
                lambda x: "#F0F0F0" if x <= tint_cutoff else "#CCCCCC"
            )(cf["count"])
        ))])
    fig_go.update_layout(title_text=title, font_size=10)
    fig_go.show()
    if export_plot:
        fig_go.write_image(save_path)
    return fig_go

def plot_time(data,col1,col2):
    r"""
    data：the predict result
    col1，col2：colname of predict time result or groundtruth
    """
    fig, ax = plt.subplots()
    sns.distplot(data[col1], color="#0278DD", hist=False, kde_kws={'bw': 0.3}, ax=ax, label=col1)
    sns.distplot(data[col2], color="#7FBE00", hist=False, kde_kws={'bw': 0.3}, ax=ax, label=col2)

