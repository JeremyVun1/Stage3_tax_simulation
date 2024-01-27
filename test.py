from tax_calc_lib import calc_tax


def test_one():
    test_brackets = {100: 0.50}
    salary = 200
    expected = 50

    actual = calc_tax(salary, test_brackets)
    assert actual == expected


def test_two():
    test_brackets = {100: 0.25, 200: 0.50, 300: 0.75}
    salary = 500
    expected = 25 + 50 + 0.75 * 200

    actual = calc_tax(salary, test_brackets)
    assert actual == expected


def run_tests():
    test_one()
    test_two()


if __name__ == "__main__":
    run_tests()
