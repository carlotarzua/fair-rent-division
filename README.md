# 🏠 Envy-Free Rent Division App

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white)

A Python-based fair division application that computes **envy-free room assignments and rent prices** for roommates. The project combines mathematical modeling, optimization, and an interactive Streamlit interface to solve a classic rent division problem.

The app uses roommate valuations to assign rooms and prices so that no person prefers another person's room at that other room's price.

---

## ✨ Features

- 🏠 **Room Assignment** — Assigns each roommate exactly one room
- 💸 **Fair Rent Pricing** — Computes room prices that add up to the total rent
- ⚖️ **Envy-Free Check** — Verifies that no roommate prefers someone else's room at the computed price
- 🧠 **Utility-Based Model** — Uses the utility formula `value - price`
- 📊 **Interactive Web App** — Built with Streamlit for easy input and visualization
- 🔢 **Linear Programming Solver** — Uses SciPy optimization to compute fair prices
- 📄 **LaTeX Report** — Includes a technical explanation of the algorithms and worked example
- 🧩 **Algorithm Comparison** — Explains both the geometric Sperner-style method and the maximin linear-programming method

---

## 🚀 Demo

> Enter each roommate's valuation for each room, choose the total rent, and compute an envy-free assignment with room prices.

![App Demo](https://your-demo-gif-or-screenshot-here.gif)

Example output:

| Person | Assigned Room | Room Price |
|---|---|---:|
| Alice | Master Bedroom | $488 |
| Bob | 2nd Floor | $13 |
| Claire | Basement | $499 |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Language** | Python 3 |
| **Web App** | Streamlit |
| **Optimization** | SciPy `linprog` |
| **Data Handling** | NumPy, pandas |
| **Mathematical Writing** | LaTeX |
| **Algorithm Type** | Fair division, linear programming, envy-free allocation |

---

## 🧠 How It Works

The rent division problem is modeled using a valuation matrix. Each roommate gives a value for every room.

If person `i` values room `j` at `vᵢⱼ`, and room `j` has price `pⱼ`, then the utility of that room is:

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

The implementation checks possible assignments and solves a linear program for each one. The selected solution maximizes the utility of the worst-off roommate while satisfying the envy-free constraints.

---

## 📐 Algorithms Explained

This project discusses two related approaches to fair rent division.

### 1. Geometric Sperner-Style Method

The geometric method represents all possible price splits as points inside a simplex. For three rooms, the simplex is a triangle.

Each point corresponds to a possible set of room prices. At each point, a roommate chooses the room that gives them the highest utility:

```text
vᵢⱼ - pⱼ
```

The triangle is subdivided into smaller triangles, and vertices are labeled according to preferred rooms. Sperner's Lemma guarantees the existence of a small fully labeled triangle. This small triangle corresponds to an approximate envy-free solution.

This method is important because it gives a geometric and constructive proof that fair rent divisions exist.

### 2. Maximin Linear-Programming Method

The implemented algorithm uses a computational optimization approach.

For each possible assignment, it solves a linear program with the following goals:

1. Room prices must add up to the total rent.
2. Each roommate must prefer their assigned room at least as much as every other room.
3. The minimum utility across all roommates should be as large as possible.

This gives an envy-free allocation while also improving the outcome of the worst-off person.

---

## 📊 Worked Example

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

Alice is indifferent between two rooms, which is allowed. Since nobody strictly prefers another person's room at that room's price, the allocation is envy-free.

---

## 📂 Project Structure

```text
envy-free-rent-division/
├── algorithm.py                         # Core fair rent division algorithm
├── app.py                               # Streamlit web app
├── requirements.txt                     # Python dependencies
├── README.md                            # Project documentation
├── examples/
│   └── three_roommates_example.json     # Example valuation matrix
└── report/
    ├── fair_rent_division_report.tex    # LaTeX source report
    ├── fair_rent_division_report.pdf    # Compiled technical report
    ├── technical_writeup.md             # Markdown write-up
    └── cv_and_portfolio_text.md         # Resume and portfolio text
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.9+
- `pip`
- Optional: LaTeX distribution if you want to compile the report locally

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/carlotarzua/envy-free-rent-division.git
   cd envy-free-rent-division
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

   Key packages:

   ```text
   streamlit
   scipy
   numpy
   pandas
   ```

---

## ▶️ Usage

### Run the Streamlit app

```bash
python -m streamlit run app.py
```

Then open the local URL shown in your terminal.

### Run the algorithm directly

```bash
python algorithm.py
```

### Use the example data

The file below contains the Alice, Bob, and Claire example:

```text
examples/three_roommates_example.json
```

You can modify it or use it as a template for other rent division problems.

---

## 📄 Technical Report

The project includes a LaTeX report explaining:

- the rent division problem,
- the utility model,
- envy-free allocation,
- the geometric Sperner-style algorithm,
- the maximin linear-programming algorithm,
- a worked numerical example,
- and a comparison between the two approaches.

The compiled report is available at:

```text
report/fair_rent_division_report.pdf
```

---

## 🌱 Future Improvements

- [ ] Add a visual triangle/simplex diagram for the Sperner-style method
- [ ] Support unequal numbers of rooms and roommates
- [ ] Add unit tests for the optimization model
- [ ] Deploy the Streamlit app online
- [ ] Add downloadable PDF or CSV results
- [ ] Add support for custom fairness objectives
- [ ] Improve mobile layout and user interface design

---

## 👩‍💻 About Me

Built by **Carlota Arzúa** — a developer interested in mathematical modeling, optimization, and applied algorithms.

- 💼 [LinkedIn](https://www.linkedin.com/in/carlota-a-53a75b206/)
- 🌐 [Portfolio](https://your-portfolio-link-here.com)
- 📧 carlotaarzua@gmail.com

---

## 📄 License

This project is intended for educational and portfolio purposes. You may adapt the code with attribution.

