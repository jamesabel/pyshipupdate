from pyshipupdate import restart_return_code, ok_return_code


def test_return_codes():
    assert ok_return_code == 0
    assert restart_return_code != 0
