# Envy-Free Rent Division Using Fair Division

This project implements a small fair-division tool for assigning rooms and rent prices among roommates.

The problem is simple to state:

> Given several roommates, several rooms, and a total rent, assign each person one room and set a price for each room so that no person would rather take another person's room at that other room's price.

This condition is called **envy-freeness**.

---

## Project features

- Python implementation of an envy-free rent division algorithm
- Linear-programming model for finding fair room prices
- Streamlit web app for interactive use
- Worked example with three roommates
- Envy check table showing why the result is fair
- Technical write-up included in `report/technical_writeup.md`

---

## Mathematical idea

Let:

- \(v_{ij}\) be person \(i\)'s value for room \(j\)
- \(p_j\) be the price of room \(j\)

The utility that person \(i\) gets from room \(j\) is:

\[
u_{ij} = v_{ij} - p_j
\]

A room assignment is envy-free when every person prefers their assigned room at least as much as every other room:

\[
v_{i,a_i} - p_{a_i} \geq v_{ij} - p_j
\]

for every person \(i\) and every room \(j\).

The algorithm checks possible assignments and solves a linear program to find room prices that satisfy the envy-free constraints. Among feasible solutions, it chooses the allocation that maximizes the minimum utility.

---

## Worked example

Total rent: **$1,000**

| Room | Alice | Bob | Claire |
|---|---:|---:|---:|
| Master Bedroom | 690 | 520 | 297 |
| Basement | 95 | 333 | 633 |
| 2nd Floor | 215 | 147 | 70 |

One fair result is:

| Person | Assigned Room | Room Price |
|---|---|---:|
| Alice | Master Bedroom | $488 |
| Bob | 2nd Floor | $13 |
| Claire | Basement | $499 |

Why this is envy-free:

| Person | Assigned utility | Best alternative utility |
|---|---:|---:|
| Alice | \(690 - 488 = 202\) | \(215 - 13 = 202\) |
| Bob | \(147 - 13 = 134\) | \(520 - 488 = 32\) |
| Claire | \(633 - 499 = 134\) | \(70 - 13 = 57\) |

Alice is tied between her room and Bob's room, which is allowed. Nobody strictly prefers someone else's room at that person's room price.

---

## How to run locally

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run app.py
```

Run the algorithm from the command line:

```bash
python algorithm.py
```

---

## Repository structure

```text
fair-rent-division/
├── README.md
├── algorithm.py
├── app.py
├── requirements.txt
├── examples/
│   └── three_roommates_example.json
└── report/
    ├── technical_writeup.md
    └── cv_and_portfolio_text.md
```

---

## Future improvements

- Add a triangle visualization inspired by Sperner's Lemma
- Support unequal numbers of people and rooms
- Add automated tests
- Add deployment instructions for Streamlit Community Cloud
- Compare this LP-based implementation with a triangulation-based approximation method
