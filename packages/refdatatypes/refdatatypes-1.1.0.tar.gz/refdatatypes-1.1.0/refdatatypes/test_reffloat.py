from refdatatypes.reffloat import Reffloat


def test_compare():
    f = Reffloat(555.0)
    assert f == 555.0
    assert f < 556.0
    assert f > 554.0
    assert f <= 556.0
    assert f >= 554.0


def test_conversfon():
    f = Reffloat(555.0)
    assert str(f) == "555.0"
    assert int(f) == 555
    assert float(f) == 555.0
    assert bool(f)


def test_math():
    f = Reffloat(555)
    f.value += 10
    assert f == 555+10
    f.value -= 20
    assert f == 555-10
