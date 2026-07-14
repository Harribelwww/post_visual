from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib as mpl

import post_visual as pv


def test_named_palettes_and_integer_aliases_cycle() -> None:
    furina = pv.get_palette("furina")
    alias = pv.get_palette(1)
    cycled = pv.get_palette("furina", n=len(furina) + 1)

    assert "furina" in pv.available_palettes()
    assert alias == furina
    assert cycled[0] == cycled[-1]


def test_style_context_is_scoped() -> None:
    before = mpl.rcParams["text.usetex"]

    with pv.style_context("nilou", usetex=True):
        assert mpl.rcParams["text.usetex"] is True
        assert mpl.rcParams["mathtext.fontset"] == "stix"

    assert mpl.rcParams["text.usetex"] == before


def test_scientific_style_uses_readable_visual_hierarchy() -> None:
    rc = pv.scientific_rc()

    assert rc["font.weight"] == "normal"
    assert rc["axes.labelweight"] == "normal"
    assert rc["axes.axisbelow"] == "line"
    assert rc["legend.fontsize"] < rc["axes.titlesize"]
