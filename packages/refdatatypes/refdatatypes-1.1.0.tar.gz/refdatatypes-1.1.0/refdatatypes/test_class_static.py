from refdatatypes.refint import RefInt


class AAA:
    static = RefInt(1)


class BBB(AAA):
    pass


def test_static():
    assert AAA.static.value == 1
    assert BBB.static.value == 1

    AAA.static.value = 5
    assert AAA.static.value == 5
    assert BBB.static.value == 5

    BBB.static.value = 6
    assert AAA.static.value == 6
    assert BBB.static.value == 6

    AAA.static.value = 7
    assert AAA.static.value == 7
    assert BBB.static.value == 7
