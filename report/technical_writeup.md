# Envy-Free Rent Division Using Fair Division

## 1. Problem statement

Rent division is a classic fair-division problem. Suppose several roommates need to divide the total rent of an apartment. The apartment has the same number of rooms as roommates, but the rooms may differ in size, quality, privacy, lighting, or location. Each person may value the rooms differently.

The goal is to assign each person one room and set a price for each room so that the prices add up to the total rent and nobody envies another person's assignment.

In this project, I implemented a computational method for finding an envy-free rent division and built a small interactive web app around it.

---

## 2. Utility model

Let:

- \(n\) be the number of roommates and rooms
- \(R\) be the total rent
- \(v_{ij}\) be person \(i\)'s value for room \(j\)
- \(p_j\) be the price of room \(j\)

The utility person \(i\) receives from room \(j\) is modeled as:

\[
u_{ij} = v_{ij} - p_j
\]

This means a room becomes more attractive when the person values it highly and less attractive when its price increases.

For an assignment \(a_i\), where person \(i\) receives room \(a_i\), the assignment is envy-free when:

\[
v_{i,a_i} - p_{a_i} \geq v_{ij} - p_j
\]

for every person \(i\) and every room \(j\).

In words: each person must like their assigned room at least as much as every other room, after prices are considered.

---

## 3. Algorithm

The algorithm has two main parts.

First, it checks every possible assignment of rooms to people. For three people, there are only \(3! = 6\) assignments. For four people, there are \(4! = 24\). This is practical for small roommate problems.

Second, for each fixed assignment, the algorithm solves a linear program to determine whether there are room prices that make that assignment envy-free.

The linear program uses the following variables:

- \(p_1, p_2, \dots, p_n\): the room prices
- \(u\): the minimum utility across all people

The constraints are:

\[
\sum_{j=1}^{n} p_j = R
\]

\[
v_{i,a_i} - p_{a_i} \geq v_{ij} - p_j
\]

for every person \(i\) and room \(j\), and

\[
v_{i,a_i} - p_{a_i} \geq u
\]

for every person \(i\).

The objective is:

\[
\text{maximize } u
\]

This means the program looks for an envy-free allocation while making the worst-off person's utility as large as possible.

---

## 4. Worked example

Consider three roommates: Alice, Bob, and Claire.

Total rent: **$1,000**

| Room | Alice | Bob | Claire |
|---|---:|---:|---:|
| Master Bedroom | 690 | 520 | 297 |
| Basement | 95 | 333 | 633 |
| 2nd Floor | 215 | 147 | 70 |

The algorithm finds this allocation:

| Person | Assigned Room | Price |
|---|---|---:|
| Alice | Master Bedroom | $488 |
| Bob | 2nd Floor | $13 |
| Claire | Basement | $499 |

Now check utilities.

For Alice:

- Master Bedroom: \(690 - 488 = 202\)
- Basement: \(95 - 499 = -404\)
- 2nd Floor: \(215 - 13 = 202\)

Alice is tied between the Master Bedroom and the 2nd Floor. Since she does not strictly prefer another person's room, this is allowed.

For Bob:

- Master Bedroom: \(520 - 488 = 32\)
- Basement: \(333 - 499 = -166\)
- 2nd Floor: \(147 - 13 = 134\)

Bob prefers his assigned room.

For Claire:

- Master Bedroom: \(297 - 488 = -191\)
- Basement: \(633 - 499 = 134\)
- 2nd Floor: \(70 - 13 = 57\)

Claire prefers her assigned room.

Therefore, the allocation is envy-free.

---

## 5. Relationship to Sperner's Lemma

A geometric way to understand this problem is to represent all possible price splits as points in a simplex. For three rooms, the simplex is a triangle. Each point in the triangle corresponds to a possible rent split among the three rooms.

At each point, a person chooses the room that maximizes \(v_{ij} - p_j\). If the triangle is divided into many smaller triangles and vertices are labeled according to preferred rooms, Sperner's Lemma guarantees the existence of a small triangle whose labels include all rooms. Such a triangle corresponds to an approximate envy-free solution.

This project implements the computational version using linear programming. A future extension would be to add a visual Sperner-style triangle demonstration to show how the geometric proof leads to an approximate fair division.

---

## 6. Implementation

The project is written in Python.

The file `algorithm.py` contains the main algorithm. The file `app.py` contains a Streamlit web interface.

The implementation:

1. accepts a valuation matrix,
2. enumerates possible room assignments,
3. solves a linear program for each assignment,
4. selects a feasible envy-free allocation, and
5. displays an envy check to verify the result.

---

## 7. Limitations

This implementation is intended for small roommate problems. Since it enumerates all assignments, the number of assignments grows factorially with the number of rooms.

For typical roommate situations with 2 to 6 people, this is fine. For much larger problems, a more scalable optimization approach would be needed.

Also, the model assumes utilities are linear in money: a person's utility is room value minus room price. This is standard for rent division, but it may not capture every real-life preference.

---

## 8. Future work

Possible extensions include:

- adding a Sperner's Lemma triangle visualization,
- supporting unequal numbers of rooms and people,
- adding tests for edge cases,
- comparing different fairness objectives,
- deploying the app publicly,
- improving the user interface for mobile devices.
