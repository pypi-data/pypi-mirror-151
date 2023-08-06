from refdatatypes.refbool import RefBool


def test_compare():
    b = RefBool(True)
    assert b == True
    assert b.value == True
    assert bool(b) == True
    assert b

    b.value = False
    assert b == False
    assert b.value == False
    assert bool(b) == False
    assert not b


def test_conversfon():
    b = RefBool(True)
    assert str(b) == "True"
    assert int(b) == 1
    assert float(b) == 1.0
    assert bool(b) == True
