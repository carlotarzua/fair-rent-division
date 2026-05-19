"""
Fair Rent Division Algorithm

This module solves an envy-free rent division problem.

Input:
    - A square valuation matrix V where V[i][j] is person i's value for room j.
    - A total rent R.
    - Optional names for people and rooms.

Output:
    - A room assignment and room prices such that no person prefers another
      room at that other room's price, when such a solution is found.
    - Among all checked assignments, the algorithm chooses the one that
      maximizes the minimum utility.

Mathematical model:
    utility(i, j) = V[i][j] - price[j]

For an assignment a_i, envy-freeness requires:

    V[i][a_i] - price[a_i] >= V[i][j] - price[j]

for every person i and every room j.

Dependencies:
    scipy
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Iterable, List, Optional, Sequence

import numpy as np
from scipy.optimize import linprog


@dataclass
class RentDivisionResult:
    people: List[str]
    rooms: List[str]
    assignment: List[int]          # assignment[i] = room index assigned to person i
    prices: np.ndarray             # prices[j] = rent for room j
    utilities: np.ndarray          # utilities[i][j] = value[i][j] - price[j]
    min_utility: float
    success: bool
    message: str

    def assignment_table(self) -> list[dict]:
        """Return a clean list of dictionaries for printing or converting to a DataFrame."""
        rows = []
        for i, room_idx in enumerate(self.assignment):
            rows.append(
                {
                    "Person": self.people[i],
                    "Assigned Room": self.rooms[room_idx],
                    "Room Price": round(float(self.prices[room_idx]), 2),
                    "Utility": round(float(self.utilities[i, room_idx]), 2),
                }
            )
        return rows

    def envy_check_table(self) -> list[dict]:
        """Return each person's assigned utility and best available utility."""
        rows = []
        for i, room_idx in enumerate(self.assignment):
            assigned_utility = float(self.utilities[i, room_idx])
            best_utility = float(np.max(self.utilities[i]))
            best_room_idx = int(np.argmax(self.utilities[i]))
            rows.append(
                {
                    "Person": self.people[i],
                    "Assigned Room": self.rooms[room_idx],
                    "Assigned Utility": round(assigned_utility, 2),
                    "Best Room at These Prices": self.rooms[best_room_idx],
                    "Best Utility": round(best_utility, 2),
                    "Envy Gap": round(assigned_utility - best_utility, 6),
                }
            )
        return rows


def _validate_inputs(
    values: Sequence[Sequence[float]],
    total_rent: float,
    people: Optional[Sequence[str]],
    rooms: Optional[Sequence[str]],
) -> tuple[np.ndarray, list[str], list[str]]:
    V = np.array(values, dtype=float)

    if V.ndim != 2:
        raise ValueError("values must be a two-dimensional matrix.")

    n_people, n_rooms = V.shape
    if n_people != n_rooms:
        raise ValueError(
            f"This implementation expects the same number of people and rooms. "
            f"Got {n_people} people and {n_rooms} rooms."
        )

    if total_rent < 0:
        raise ValueError("total_rent must be nonnegative.")

    if people is None:
        people = [f"Person {i + 1}" for i in range(n_people)]
    else:
        people = list(people)

    if rooms is None:
        rooms = [f"Room {j + 1}" for j in range(n_rooms)]
    else:
        rooms = list(rooms)

    if len(people) != n_people:
        raise ValueError("The number of people names must match the number of rows in values.")

    if len(rooms) != n_rooms:
        raise ValueError("The number of room names must match the number of columns in values.")

    return V, people, rooms


def solve_assignment_lp(
    values: np.ndarray,
    assignment: Sequence[int],
    total_rent: float,
    *,
    allow_negative_prices: bool = True,
) -> Optional[tuple[np.ndarray, float]]:
    """Solve the rent-pricing LP for one fixed room assignment.

    Variables are:
        p_1, ..., p_n, u

    where p_j is room j's rent and u is the minimum utility.

    Objective:
        maximize u

    Constraints:
        sum_j p_j = total_rent

        V[i][a_i] - p[a_i] >= V[i][j] - p[j]
        for every person i and room j

        V[i][a_i] - p[a_i] >= u
        for every person i
    """

    n = values.shape[0]
    assignment = list(assignment)

    # Objective: linprog minimizes, so maximize u by minimizing -u.
    c = np.zeros(n + 1)
    c[-1] = -1

    A_ub = []
    b_ub = []

    # Envy-free constraints.
    for i, assigned_room in enumerate(assignment):
        for other_room in range(n):
            row = np.zeros(n + 1)
            row[assigned_room] += 1
            row[other_room] -= 1
            A_ub.append(row)
            b_ub.append(values[i, assigned_room] - values[i, other_room])

    # Minimum-utility constraints.
    # V[i][assigned_room] - p[assigned_room] >= u
    # p[assigned_room] + u <= V[i][assigned_room]
    for i, assigned_room in enumerate(assignment):
        row = np.zeros(n + 1)
        row[assigned_room] = 1
        row[-1] = 1
        A_ub.append(row)
        b_ub.append(values[i, assigned_room])

    A_eq = [np.r_[np.ones(n), 0]]
    b_eq = [total_rent]

    price_bounds = (None, None) if allow_negative_prices else (0, None)
    bounds = [price_bounds for _ in range(n)] + [(None, None)]

    result = linprog(
        c,
        A_ub=np.array(A_ub),
        b_ub=np.array(b_ub),
        A_eq=np.array(A_eq),
        b_eq=np.array(b_eq),
        bounds=bounds,
        method="highs",
    )

    if not result.success:
        return None

    prices = result.x[:n]
    min_utility = result.x[-1]
    return prices, min_utility


def solve_fair_rent(
    values: Sequence[Sequence[float]],
    total_rent: float,
    people: Optional[Sequence[str]] = None,
    rooms: Optional[Sequence[str]] = None,
    *,
    allow_negative_prices: bool = True,
) -> RentDivisionResult:
    """Find a fair rent division by checking every possible assignment.

    This is practical for small roommate problems. For example:
        3 rooms -> 6 assignments
        4 rooms -> 24 assignments
        5 rooms -> 120 assignments
        6 rooms -> 720 assignments

    For each assignment, a linear program finds prices that make that assignment
    envy-free and maximize the minimum utility. The best assignment overall is
    selected.
    """

    V, people, rooms = _validate_inputs(values, total_rent, people, rooms)
    n = V.shape[0]

    best_assignment = None
    best_prices = None
    best_min_utility = -np.inf

    for assignment in permutations(range(n)):
        solved = solve_assignment_lp(
            V,
            assignment,
            total_rent,
            allow_negative_prices=allow_negative_prices,
        )

        if solved is None:
            continue

        prices, min_utility = solved

        # Tie-breaker: prefer a solution with smaller price spread.
        price_spread = float(np.max(prices) - np.min(prices))
        if best_prices is None:
            is_better = True
        else:
            best_spread = float(np.max(best_prices) - np.min(best_prices))
            is_better = (
                min_utility > best_min_utility + 1e-8
                or (
                    abs(min_utility - best_min_utility) <= 1e-8
                    and price_spread < best_spread
                )
            )

        if is_better:
            best_assignment = list(assignment)
            best_prices = prices
            best_min_utility = float(min_utility)

    if best_assignment is None or best_prices is None:
        return RentDivisionResult(
            people=people,
            rooms=rooms,
            assignment=[],
            prices=np.array([]),
            utilities=np.array([]),
            min_utility=float("nan"),
            success=False,
            message="No feasible envy-free price system was found.",
        )

    utilities = V - best_prices.reshape(1, -1)

    return RentDivisionResult(
        people=people,
        rooms=rooms,
        assignment=best_assignment,
        prices=best_prices,
        utilities=utilities,
        min_utility=best_min_utility,
        success=True,
        message="Found an envy-free rent division.",
    )


if __name__ == "__main__":
    people = ["Alice", "Bob", "Claire"]
    rooms = ["Master Bedroom", "Basement", "2nd Floor"]
    total_rent = 1000

    values = [
        [690, 95, 215],
        [520, 333, 147],
        [297, 633, 70],
    ]

    result = solve_fair_rent(values, total_rent, people, rooms)

    print(result.message)
    print("\nAssignment:")
    for row in result.assignment_table():
        print(row)

    print("\nEnvy check:")
    for row in result.envy_check_table():
        print(row)
