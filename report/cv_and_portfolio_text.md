# CV and Portfolio Text

## CV version

**Envy-Free Rent Division Algorithm**  
Personal Project / Mathematical Modeling Project

- Implemented a Python tool for assigning rooms and rent prices among roommates using fair-division principles.
- Modeled roommate preferences with valuation matrices and utility functions of the form `value - price`.
- Formulated envy-free rent division as a linear-programming problem with constraints ensuring no roommate prefers another person's room at that room's price.
- Built an interactive Streamlit web app for users to enter room valuations and compute fair assignments.
- Verified results with utility tables showing each person's assigned utility compared with their best available alternative.

---

## Short resume version

**Envy-Free Rent Division Web App**  
Built a Python and Streamlit application that computes fair room assignments and rent prices using utility maximization and envy-free fair division. Implemented a linear-programming model, added example data, and generated verification tables showing that no roommate envies another assignment.

---

## Portfolio project page

### Envy-Free Rent Division Using Fair Division

**Type:** Mathematical Modeling / Algorithms / Python / Streamlit

**Goal:**  
Create an interactive tool that fairly assigns rooms and rent prices among roommates.

**Overview:**  
This project solves a fair-division problem known as rent division. Each roommate assigns values to each room, and the program computes both a room assignment and room prices. The result is envy-free, meaning no person prefers another person's room at that person's assigned price.

**Methods used:**

- Fair division
- Utility maximization
- Envy-free allocation
- Linear programming
- Python
- Streamlit

**What I built:**

- A Python algorithm that checks possible room assignments
- A linear-programming model for computing fair prices
- A Streamlit web interface for entering values and displaying results
- A worked example with Alice, Bob, and Claire
- Utility tables that verify whether the final allocation is envy-free

**Result:**  
The app computes an assignment and rent split where each person receives a room that maximizes or ties their utility at the computed prices.

**Example:**  
For a $1,000 rent split among Alice, Bob, and Claire, the app assigns Alice to the Master Bedroom, Bob to the 2nd Floor, and Claire to the Basement, with prices chosen so that no one envies another room.

---

## GitHub repository description

A Python and Streamlit implementation of envy-free rent division. The app lets roommates enter valuations for rooms and computes room assignments and prices using a linear-programming model.

---

## LinkedIn project description

I built an interactive fair-division tool for rent splitting. The project models each roommate's utility as `room value - room price` and computes an envy-free allocation using Python and linear programming. I also created a Streamlit web app so users can enter their own room valuations and see the final assignment, prices, and envy-check table.
