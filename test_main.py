from main import calculate_addition


def test_addition():
    assert calculate_addition(1, 3) == 4
    assert calculate_addition(12, 3) == 15
    print("test_addition - Passed!")
