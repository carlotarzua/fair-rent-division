# Deployment Guide

This project is structured for Streamlit Community Cloud.

## 1. Push the project to GitHub

Create a repository named something like:

```text
envy-free-rent-division
```

Then upload or push these files:

```text
app.py
algorithm.py
requirements.txt
README.md
examples/
report/
```

## 2. Deploy on Streamlit Community Cloud

When creating the app, use:

```text
Main file path: app.py
```

Streamlit will install packages from `requirements.txt`.

## 3. After deployment

Open the deployed app and test the default example:

- Total rent: `1000`
- People: `Alice`, `Bob`, `Claire`
- Rooms: `Master Bedroom`, `Basement`, `2nd Floor`

Expected assignment:

| Person | Assigned Room | Approximate Price |
|---|---|---:|
| Alice | Master Bedroom | 488 |
| Bob | 2nd Floor | 13 |
| Claire | Basement | 499 |

## 4. Recommended GitHub repo settings

- Add a short repo description: `Streamlit app for envy-free rent division using linear programming.`
- Add topics: `python`, `streamlit`, `optimization`, `linear-programming`, `fair-division`, `scipy`.
- Pin the repo on your GitHub profile while applying for internships.

## 5. Suggested LinkedIn/GitHub description

> Built an interactive fair-division web app that computes envy-free room assignments and rent prices using a maximin linear-programming model. Implemented the optimization algorithm in Python with SciPy, built the interface in Streamlit, and documented the mathematical background with a technical report.
