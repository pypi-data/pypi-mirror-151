from refdatatypes.refint import RefInt


def test_addresses():
    i = RefInt(555)
    r_addr = i.get_ref_addr()
    v_addr = i.get_value_addr()
    i.value = 556
    assert r_addr == i.get_ref_addr()
    assert v_addr != i.get_value_addr()


def test_compare():
    i = RefInt(555)
    assert i == 555
    assert i < 556
    assert i > 554
    assert i <= 556
    assert i >= 554
    assert i != 0


def test_conversion():
    i = RefInt(555)
    assert str(i) == "555"
    assert int(i) == 555
    assert float(i) == 555.0
    assert bool(i)


def test_math():
    i = RefInt(555)
    i.value += 10
    assert i == 555+10
    i.value -= 20
    assert i == 555-10
