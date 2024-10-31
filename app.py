import streamlit as st
import pandas as pd

# Set up Streamlit page configuration
st.set_page_config(page_title="Ivy League Universities Information", layout="wide")

# Page title
st.title("📚 Ivy League Universities Information")

# Ivy League universities data
ivy_league_data = {
    "University": [
        "Harvard University", "Yale University", "Princeton University", "Columbia University",
        "University of Pennsylvania", "Dartmouth College", "Brown University", "Cornell University"
    ],
    "Location": [
        "Cambridge, MA", "New Haven, CT", "Princeton, NJ", "New York, NY",
        "Philadelphia, PA", "Hanover, NH", "Providence, RI", "Ithaca, NY"
    ],
    "Acceptance Rate": [3.4, 4.6, 3.8, 5.1, 5.9, 7.9, 6.9, 10.7],
    "Undergraduate Enrollment": [6980, 6249, 5310, 8610, 10495, 4321, 7322, 15043],
    "Tuition (2024)": [
        "$57,246", "$64,700", "$57,410", "$65,524", "$63,452", "$63,984", "$65,696", "$63,200"
    ],
    "Notable Alumni": [
        "Mark Zuckerberg, Barack Obama", "George H.W. Bush, Jodie Foster", 
        "Michelle Obama, Jeff Bezos", "Ruth Bader Ginsburg, Warren Buffett", 
        "Elon Musk, Donald Trump", "Nelson Rockefeller, Dr. Seuss",
        "Emma Watson, John F. Kennedy Jr.", "Ruth Bader Ginsburg, Toni Morrison"
    ]
}

# Convert data to DataFrame
df_ivy = pd.DataFrame(ivy_league_data)

# Sidebar filters
st.sidebar.title("Filter Universities")
min_acceptance_rate = st.sidebar.slider("Maximum Acceptance Rate (%)", min_value=1.0, max_value=15.0, value=10.0)
min_undergrad_enrollment = st.sidebar.slider("Minimum Undergraduate Enrollment", min_value=1000, max_value=20000, value=5000)

# Filter data based on sidebar inputs
filtered_df = df_ivy[
    (df_ivy["Acceptance Rate"] <= min_acceptance_rate) &
    (df_ivy["Undergraduate Enrollment"] >= min_undergrad_enrollment)
]

# Display filtered data
st.subheader("Ivy League Universities Information")
st.dataframe(filtered_df)

# Display individual university details
st.sidebar.title("University Details")
selected_university = st.sidebar.selectbox("Select a university", df_ivy["University"])

st.sidebar.subheader(f"Details for {selected_university}")
university_info = df_ivy[df_ivy["University"] == selected_university].iloc[0]

st.sidebar.write(f"**Location:** {university_info['Location']}")
st.sidebar.write(f"**Acceptance Rate:** {university_info['Acceptance Rate']}%")
st.sidebar.write(f"**Undergraduate Enrollment:** {university_info['Undergraduate Enrollment']}")
st.sidebar.write(f"**Tuition (2024):** {university_info['Tuition (2024)']}")
st.sidebar.write(f"**Notable Alumni:** {university_info['Notable Alumni']}")

# Charts for visual representation
st.subheader("Acceptance Rate and Enrollment Comparison")

# Bar chart for acceptance rate
st.write("### Acceptance Rate Comparison")
st.bar_chart(df_ivy.set_index("University")["Acceptance Rate"])

# Bar chart for undergraduate enrollment
st.write("### Undergraduate Enrollment Comparison")
st.bar_chart(df_ivy.set_index("University")["Undergraduate Enrollment"])

# Tuition bar chart
st.write("### Tuition Fees Comparison (2024)")
tuition_fees = df_ivy.set_index("University")["Tuition (2024)"].replace('[\$,]', '', regex=True).astype(float)
st.bar_chart(tuition_fees)
