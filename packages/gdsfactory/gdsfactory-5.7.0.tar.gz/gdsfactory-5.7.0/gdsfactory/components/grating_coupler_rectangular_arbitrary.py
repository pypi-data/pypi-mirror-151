from typing import Optional, Tuple

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.rectangle import rectangle
from gdsfactory.components.taper import taper as taper_function
from gdsfactory.tech import LAYER
from gdsfactory.types import ComponentSpec, Floats, Layer

_gaps = (0.2,) * 10
_widths = (0.5,) * 10


@gf.cell
def grating_coupler_rectangular_arbitrary(
    gaps: Floats = _gaps,
    widths: Floats = _widths,
    wg_width: float = 0.5,
    width_grating: float = 11.0,
    length_taper: float = 150.0,
    layer: Tuple[int, int] = gf.LAYER.WG,
    polarization: str = "te",
    wavelength: float = 1.55,
    taper: Optional[ComponentSpec] = taper_function,
    layer_slab: Optional[Tuple[int, int]] = LAYER.SLAB150,
    slab_xmin: float = -1.0,
    slab_offset: float = 1.0,
    fiber_marker_layer: Layer = gf.LAYER.TE,
) -> Component:
    r"""Grating coupler uniform (grating with rectangular shape not elliptical).
    Therefore it needs a longer taper.
    Grating teeth are straight instead of elliptical.

    Args:
        gaps: list of gaps between grating teeth.
        widths: list of grating widths.
        wg_width: input waveguide width.
        width_grating: grating teeth width.
        length_taper: taper length (um).
        layer: for grating teeth.
        polarization: 'te' or 'tm'.
        wavelength: in um.
        taper: function.
        layer_slab: layer that protects the slab under the grating.
        slab_xmin: where 0 is at the start of the taper.
        slab_offset: from edge of grating to edge of the slab.

    .. code::

                      fiber

                   /  /  /  /
                  /  /  /  /

                _|-|_|-|_|-|___ layer
                   layer_slab |
            o1  ______________|



        top view     _________
                    /| | | | |
                   / | | | | |
                  /taper_angle
                 /_ _| | | | |
        wg_width |   | | | | |
                 \   | | | | |
                  \  | | | | |
                   \ | | | | |
                    \|_|_|_|_|
                 <-->
                taper_length

    """
    c = Component()

    if taper:
        taper_ref = c << taper(
            length=length_taper,
            width2=width_grating,
            width1=wg_width,
            layer=layer,
        )

        c.add_port(port=taper_ref.ports["o1"], name="o1")
        xi = taper_ref.xmax
    else:
        length_taper = 0
        xi = 0

    widths = gf.snap.snap_to_grid(widths)
    gaps = gf.snap.snap_to_grid(gaps)

    for width, gap in zip(widths, gaps):
        xi += gap + width / 2
        cgrating = c.add_ref(
            rectangle(
                size=[width, width_grating],
                layer=layer,
                port_type=None,
                centered=True,
            )
        )
        cgrating.x = gf.snap.snap_to_grid(xi)
        cgrating.y = 0
        xi += width / 2

    if layer_slab:
        slab_xmin += length_taper
        slab_xsize = xi + slab_offset
        slab_ysize = c.ysize + 2 * slab_offset
        yslab = slab_ysize / 2
        c.add_polygon(
            [
                (slab_xmin, yslab),
                (slab_xsize, yslab),
                (slab_xsize, -yslab),
                (slab_xmin, -yslab),
            ],
            layer_slab,
        )
    xport = np.round((xi + length_taper) / 2, 3)
    port_type = f"vertical_{polarization.lower()}"
    c.add_port(
        name=port_type,
        port_type=port_type,
        midpoint=(xport, 0),
        orientation=0,
        width=width_grating,
        layer=fiber_marker_layer,
    )
    c.info["polarization"] = polarization
    c.info["wavelength"] = wavelength
    gf.asserts.grating_coupler(c)
    return c


if __name__ == "__main__":
    c = grating_coupler_rectangular_arbitrary()
    print(c.ports)
    c.show()
