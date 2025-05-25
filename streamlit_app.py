# Property Tax Revaluation Web App using Streamlit

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Property Tax Revaluation Simulator")

# Explanation Panel
st.markdown("""
### 📘 How This Works
This simulator assumes a **fixed municipal budget** and calculates how property taxes are redistributed when values change due to revaluation.

- The **total tax levy stays constant**.
- The **mill rate adjusts** based on the Net Grand List.
- **More expensive homes always pay more**—what changes is how much **more or less** each property pays **relative to others**.
- If your property's value **rises faster than the town average**, your share of the tax burden increases.
- If it rises **slower**, your share decreases.

**Revaluations do not raise more money for the city—they just redistribute who pays what.**
""")

# Sidebar Inputs
st.sidebar.header("Inputs")
budget = st.sidebar.slider("Total Municipal Budget ($)", min_value=500000, max_value=5000000, value=1000000, step=50000)
num_properties = st.sidebar.slider("Number of Properties", 3, 10, 5)

st.sidebar.markdown("---")

pre_values = []
post_values = []

for i in range(num_properties):
    pre = st.sidebar.number_input(f"Home {chr(65+i)} Pre-Reval Value ($)", min_value=100000, value=200000 + i * 50000, step=10000)
    post = st.sidebar.number_input(f"Home {chr(65+i)} Post-Reval Value ($)", min_value=100000, value=pre + 40000, step=10000)
    pre_values.append(pre)
    post_values.append(post)

# Simulate property tax allocation
def simulate_property_tax(home_values_pre, home_values_post, budget):
    df = pd.DataFrame({
        "Homeowner": [chr(65 + i) for i in range(len(home_values_pre))],
        "Pre-Reval Value ($)": home_values_pre,
        "Post-Reval Value ($)": home_values_post
    })

    pre_total = sum(home_values_pre)
    post_total = sum(home_values_post)

    df["Pre Tax ($)"] = [round(val / pre_total * budget) for val in home_values_pre]
    df["Post Tax ($)"] = [round(val / post_total * budget) for val in home_values_post]
    df["Tax Change ($)"] = df["Post Tax ($)"] - df["Pre Tax ($)"]
    df["% Change"] = ((df["Tax Change ($)"] / df["Pre Tax ($)"]) * 100).round().astype(int).astype(str) + "%"

    mill_rate_pre = round(budget / pre_total * 1000, 2)
    mill_rate_post = round(budget / post_total * 1000, 2)

    return df, mill_rate_pre, mill_rate_post

# Run simulation and display results
if st.button("Run Simulation"):
    result_df, mill_rate_pre, mill_rate_post = simulate_property_tax(pre_values, post_values, budget)
    st.subheader("Tax Redistribution Results")
    st.dataframe(result_df, use_container_width=True)

    st.markdown(f"**Mill Rate Before Revaluation:** {mill_rate_pre}")
    st.markdown(f"**Mill Rate After Revaluation:** {mill_rate_post}")

    # Optional: Bar chart
    st.subheader("Tax Comparison Before and After")
    fig, ax = plt.subplots(figsize=(10, 5))
    x = result_df['Homeowner']
    ax.bar(x, result_df['Pre Tax ($)'], width=0.4, label='Pre-Tax', align='edge')
    ax.bar(x, result_df['Post Tax ($)'], width=-0.4, label='Post-Tax', align='edge')
    ax.set_ylabel("Tax Amount ($)")
    ax.set_xlabel("Homeowner")
    ax.legend()
    st.pyplot(fig)
