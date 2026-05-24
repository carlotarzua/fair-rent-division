# 🏠 Envy-Free Rent Division App

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white)

A Python + Streamlit application that computes **envy-free room assignments and rent prices** for roommates.

This project combines mathematical modeling, linear programming, and an interactive web interface to solve a classic fair-division problem: assign each person one room and choose room prices so that nobody prefers another person's room at that other room's price.

---

## Why this project is useful

This is a portfolio-friendly project because it demonstrates:

- mathematical modeling with utility functions,
- linear programming with `scipy.optimize.linprog`,
- algorithm design using assignment enumeration,
- interactive app development with Streamlit,
- data handling with NumPy and pandas,
- technical communication through a LaTeX report and worked example.

---

## Features

- 🏠 **Room assignment** — assigns each roommate exactly one room
- 💸 **Fair rent pricing** — computes room prices that add up to the total rent
- ⚖️ **Envy-free verification** — checks whether anyone prefers another room at its computed price
- 🧠 **Utility model** — uses `utility = room value - room price`
- 📊 **Interactive Streamlit UI** — edit valuations directly in the browser
- 🔢 **Linear programming solver** — computes fair prices with SciPy
- 📥 **CSV export** — download the final assignment table
- 📄 **Technical report** — includes the mathematical background and worked example

---

## Demo

Enter each roommate's valuation for each room, choose the total rent, and click **Compute envy-free rent division**.

Example output for a $1,000 rent split:

| Person | Assigned Room | Room Price | Utility |
|---|---|---:|---:|
| Alice | Master Bedroom | $488 | 202 |
| Bob | 2nd Floor | $13 | 134 |
| Claire | Basement | $499 | 134 |

The app also displays an envy-check table and a full utility matrix so the result can be verified.

---

## Tech stack

| Component | Technology |
|---|---|
| Language | Python 3 |
| Web app | Streamlit |
| Optimization | SciPy `linprog` |
| Data handling | NumPy, pandas |
| Mathematical writing | LaTeX |
| Algorithm type | Fair division, linear programming, envy-free allocation |

---

## How it works

Each roommate gives a value for every room. If person `i` values room `j` at `vᵢⱼ`, and room `j` has price `pⱼ`, then the utility of that room is:

```text
utility = value - price
```

or mathematically:

```text
uᵢⱼ = vᵢⱼ - pⱼ
```

A solution is **envy-free** when every person receives a room that gives them at least as much utility as every other room at the computed prices.

```text
Input valuations
        │
        ▼
Generate possible room assignments
        │
        ▼
For each assignment, solve rent-pricing constraints
        │
        ▼
Check envy-free inequalities
        │
        ▼
Choose the assignment maximizing minimum utility
        │
        ▼
Display assignment, prices, and envy check
```

The implemented algorithm checks possible assignments and solves a linear program for each one. The selected solution maximizes the utility of the worst-off roommate while satisfying the envy-free constraints.

---

## Worked example

Total rent: **$1,000**

| Room | Alice | Bob | Claire |
|---|---:|---:|---:|
| Master Bedroom | 690 | 520 | 297 |
| Basement | 95 | 333 | 633 |
| 2nd Floor | 215 | 147 | 70 |

One envy-free result is:

| Person | Assigned Room | Room Price |
|---|---|---:|
| Alice | Master Bedroom | $488 |
| Bob | 2nd Floor | $13 |
| Claire | Basement | $499 |

Utility check:

| Person | Own Room Utility | Best Alternative Utility | Envy-Free? |
|---|---:|---:|---|
| Alice | `690 - 488 = 202` | `215 - 13 = 202` | Yes, tied |
| Bob | `147 - 13 = 134` | `520 - 488 = 32` | Yes |
| Claire | `633 - 499 = 134` | `70 - 13 = 57` | Yes |

Alice is indifferent between two rooms, which is allowed. Since nobody strictly prefers another person's room at that other room's price, the allocation is envy-free.

---

## Project structure

```text
envy-free-rent-division/
├── app.py                               # Streamlit web app
├── algorithm.py                         # Core fair rent division algorithm
├── requirements.txt                     # Deployment dependencies
├── README.md                            # Project documentation
├── deployment.md                        # Deployment instructions
├── examples/
│   └── three_roommates_example.json     # Example valuation matrix
├── report/
│   ├── fair_rent_division_report.pdf    # Compiled technical report
│   ├── fair_rent_division_report.tex    # LaTeX source report
│   └── technical_writeup.md             # Markdown write-up
└── tests/
    └── test_algorithm.py                # Basic algorithm regression test
```

---

## Getting started

### Prerequisites

- Python 3.9+
- `pip`
- Optional: a LaTeX distribution if you want to compile the report locally

### Installation

```bash
git clone https://github.com/carlotarzua/envy-free-rent-division.git
cd envy-free-rent-division
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Run the algorithm directly

```bash
python algorithm.py
```

---

## Deployment

This project is ready to deploy on Streamlit Community Cloud.

Use this main file path:

```text
app.py
```

The deployment service should install dependencies from:

```text
requirements.txt
```

See `DEPLOYMENT.md` for step-by-step deployment notes.

---

## Limitations and future improvements

- The current app supports the same number of rooms and roommates.
- The algorithm enumerates all assignments, so it is intended for small roommate groups.
- The model assumes quasi-linear utilities: `value - price`.
- Future work could add a Sperner triangle visualization, unequal numbers of rooms and roommates, extra fairness objectives, and stronger unit tests.

---

## About me

Built by **Carlota Arzúa**, a developer interested in mathematical modeling, optimization, and applied algorithms.

- LinkedIn: https://www.linkedin.com/in/carlota-a-53a75b206/
- Email: carlotaarzua@gmail.com

---

## License

This project is intended for educational and portfolio purposes. You may adapt the code with attribution.
