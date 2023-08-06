import gdsfactory as gf


def test_path_less_than_1nm() -> None:
    c = gf.components.straight(length=0.5e-3)
    assert not c.references
    assert not c.polygons


if __name__ == "__main__":
    c = gf.components.straight(length=0.5e-3)
    c.show()
