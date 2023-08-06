"""Adiabatic tapers from CSV files
"""
import pathlib
from functools import partial
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

import gdsfactory as gf
from gdsfactory.component import Component

data = pathlib.Path(__file__).parent / "csv_data"


@gf.cell
def taper_from_csv(
    filepath: Path = data / "taper_strip_0p5_3_36.csv",
    layer: Tuple[int, int] = (1, 0),
    layer_cladding: Tuple[int, int] = gf.LAYER.WGCLAD,
    cladding_offset: float = 3.0,
) -> Component:
    """Returns taper from CSV file.

    Args:
        filepath: for CSV file.
        layer: for taper.
        layer_cladding: for cladding.
        cladding_offset: in um.

    """
    taper_data = pd.read_csv(filepath)
    xs = taper_data["x"].values * 1e6
    ys = np.round(taper_data["width"].values * 1e6 / 2.0, 3)
    ys_trench = ys + cladding_offset

    c = gf.Component()
    c.add_polygon(list(zip(xs, ys)) + list(zip(xs, -ys))[::-1], layer=layer)
    c.add_polygon(
        list(zip(xs, ys_trench)) + list(zip(xs, -ys_trench))[::-1], layer=layer_cladding
    )

    c.add_port(
        name="o1", midpoint=(xs[0], 0), width=2 * ys[0], orientation=180, layer=layer
    )
    c.add_port(
        name="o2", midpoint=(xs[-1], 0), width=2 * ys[-1], orientation=0, layer=layer
    )
    return c


taper_0p5_to_3_l36 = partial(taper_from_csv, filepath=data / "taper_strip_0p5_3_36.csv")
taper_w10_l100 = partial(taper_from_csv, filepath=data / "taper_strip_0p5_10_100.csv")
taper_w10_l150 = partial(taper_from_csv, filepath=data / "taper_strip_0p5_10_150.csv")
taper_w10_l200 = partial(taper_from_csv, filepath=data / "taper_strip_0p5_10_200.csv")
taper_w11_l200 = partial(taper_from_csv, filepath=data / "taper_strip_0p5_11_200.csv")
taper_w12_l200 = partial(taper_from_csv, filepath=data / "taper_strip_0p5_12_200.csv")


if __name__ == "__main__":
    # c = taper_0p5_to_3_l36()
    c = taper_w10_l100()
    # c = taper_w11_l200()
    c.show()
