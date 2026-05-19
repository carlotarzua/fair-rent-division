"""
Streamlit web app for the Fair Rent Division project.

Run locally:
    streamlit run app.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from algorithm import solve_fair_rent


st.set_page_config(
    page_title="Fair Rent Division",
    page_icon="🏠",
    layout="wide",
)

st.title("🏠 Envy-Free Rent Division")
st.caption("A small fair-division tool for assigning rooms and rent prices.")

with st.expander("What does this app do?", expanded=True):
    st.markdown(
        """
        This app solves a rent division problem. Each roommate gives a value for
        each room. The algorithm chooses:

        1. which person gets which room, and
        2. how much each room costs,

        so that no person prefers another person's room at that other room's price.

        The utility model is:

        `utility = value of room - room price`

        A solution is **envy-free** when every person receives a room that gives
        them at least as much utility as every other room at the computed prices.
        """
    )

st.sidebar.header("Problem settings")

total_rent = st.sidebar.number_input(
    "Total rent",
    min_value=0.0,
    value=1000.0,
    step=50.0,
)

n = st.sidebar.slider(
    "Number of roommates / rooms",
    min_value=2,
    max_value=6,
    value=3,
)

allow_negative_prices = st.sidebar.checkbox(
    "Allow negative room prices",
    value=True,
    help=(
        "In some fair-division models, a bad room can receive a negative price. "
        "Turn this off if every room price must be at least zero."
    ),
)

default_people = ["Alice", "Bob", "Claire", "Diego", "Eva", "Fatima"][:n]
default_rooms = [
    "Master Bedroom",
    "Basement",
    "2nd Floor",
    "Small Room",
    "Studio",
    "Loft",
][:n]

st.subheader("1. Enter names")

name_cols = st.columns(2)

with name_cols[0]:
    people_text = st.text_area(
        "People, one per line",
        value="\n".join(default_people),
        height=150,
    )

with name_cols[1]:
    rooms_text = st.text_area(
        "Rooms, one per line",
        value="\n".join(default_rooms),
        height=150,
    )

people = [x.strip() for x in people_text.splitlines() if x.strip()]
rooms = [x.strip() for x in rooms_text.splitlines() if x.strip()]

if len(people) != n or len(rooms) != n:
    st.warning(f"Please enter exactly {n} people and {n} rooms.")
    st.stop()

st.subheader("2. Enter each person's value for each room")

if n == 3:
    default_values = pd.DataFrame(
        {
            people[0]: [690.0, 95.0, 215.0],
            people[1]: [520.0, 333.0, 147.0],
            people[2]: [297.0, 633.0, 70.0],
        },
        index=rooms,
    )
else:
    equal_value = total_rent / n if n else 0
    default_values = pd.DataFrame(
        {person: [equal_value for _ in rooms] for person in people},
        index=rooms,
    )

st.write(
    "Rows are rooms. Columns are people. "
    "For standard rent division, each person's column should add up to the total rent."
)

edited = st.data_editor(
    default_values,
    use_container_width=True,
    num_rows="fixed",
)

column_sums = edited.sum(axis=0)
sum_table = pd.DataFrame(
    {
        "Person": column_sums.index,
        "Total Valuation": column_sums.values,
        "Difference from Total Rent": column_sums.values - total_rent,
    }
)

with st.expander("Check valuation totals"):
    st.dataframe(sum_table, use_container_width=True)

    if any(abs(column_sums - total_rent) > 1e-6):
        st.info(
            "Some columns do not add up to the total rent. The algorithm can still run, "
            "but the standard roommate-rent interpretation works best when each person "
            "distributes the total rent across the rooms."
        )

st.subheader("3. Compute fair division")

if st.button("Compute envy-free rent division", type="primary"):
    try:
        # app table is rooms x people; algorithm expects people x rooms
        values = edited.T.values

        result = solve_fair_rent(
            values,
            total_rent,
            people=people,
            rooms=rooms,
            allow_negative_prices=allow_negative_prices,
        )

        if not result.success:
            st.error(result.message)
            st.stop()

        st.success(result.message)

        assignment_df = pd.DataFrame(result.assignment_table())
        prices_df = pd.DataFrame(
            {
                "Room": rooms,
                "Price": [round(float(p), 2) for p in result.prices],
            }
        )
        envy_df = pd.DataFrame(result.envy_check_table())
        utilities_df = pd.DataFrame(
            result.utilities,
            index=people,
            columns=rooms,
        ).round(2)

        left, right = st.columns(2)

        with left:
            st.markdown("### Assignment")
            st.dataframe(assignment_df, use_container_width=True, hide_index=True)

        with right:
            st.markdown("### Room prices")
            st.dataframe(prices_df, use_container_width=True, hide_index=True)

        st.markdown("### Envy check")
        st.write(
            "The envy gap is assigned utility minus best utility. "
            "A value of 0 means the person is tied between their room and another room. "
            "A negative value would indicate envy."
        )
        st.dataframe(envy_df, use_container_width=True, hide_index=True)

        st.markdown("### Full utility matrix")
        st.dataframe(utilities_df, use_container_width=True)

        csv = assignment_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download assignment as CSV",
            data=csv,
            file_name="fair_rent_assignment.csv",
            mime="text/csv",
        )

    except Exception as exc:
        st.error(f"Something went wrong: {exc}")
