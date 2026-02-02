import streamlit as st
import pandas as pd

# -------------------------------
# CONFIG
# -------------------------------
APP_PASSWORD = "Lex-Aura123%"  # change this before selling

st.set_page_config(page_title="Excel & CSV Data Cleaner", layout="centered")

# -------------------------------
# PASSWORD GATE
# -------------------------------
st.title("Excel & CSV Data Cleaner")

password = st.text_input("Enter access password", type="password")

if password != APP_PASSWORD:
    st.warning("Please enter the correct password to continue.")
    st.stop()

# -------------------------------
# APP UI
# -------------------------------
st.success("Access granted")

uploaded_file = st.file_uploader(
    "Upload your Excel or CSV file",
    type=["csv", "xlsx"]
)

remove_duplicates = st.checkbox("Remove duplicate rows", value=True)
fix_columns = st.checkbox("Fix column names", value=True)
fill_missing = st.checkbox("Fill missing values", value=True)
fix_dates = st.checkbox("Fix date columns", value=True)

if uploaded_file is not None:
    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Preview of uploaded data")
    st.dataframe(df.head())

    if st.button("Clean Data"):
        # Clean column names
        if fix_columns:
            df.columns = (
                df.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_")
            )

        # Remove duplicates
        if remove_duplicates:
            df = df.drop_duplicates()

        # Fix dates
        if fix_dates:
            for col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass

        # Fill missing values
        if fill_missing:
            df = df.fillna("Not Available")

        st.success("Data cleaned successfully!")

        # Download
        output_file = "cleaned_data.xlsx"
        df.to_excel(output_file, index=False)

        with open(output_file, "rb") as f:
            st.download_button(
                label="Download cleaned Excel file",
                data=f,
                file_name=output_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
