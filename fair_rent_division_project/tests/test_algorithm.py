from algorithm import solve_fair_rent


def test_three_roommates_example_is_envy_free():
    people = ["Alice", "Bob", "Claire"]
    rooms = ["Master Bedroom", "Basement", "2nd Floor"]
    values = [
        [690, 95, 215],
        [520, 333, 147],
        [297, 633, 70],
    ]

    result = solve_fair_rent(values, 1000, people, rooms)

    assert result.success
    assert round(float(result.prices.sum()), 6) == 1000

    for row in result.envy_check_table():
        assert row["Envy Gap"] >= -1e-6
