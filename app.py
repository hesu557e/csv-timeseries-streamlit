import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="CSV Time-Series Visualizer",
    layout="centered"
)


st.title("📈 CSV Time-Series Visualizer")

st.markdown(
    """
Upload a CSV file and visualize selected columns easily.
"""
)


# -------------------------
# File Upload
# -------------------------
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)


if uploaded_file is not None:

    # Read CSV (default: first row = header)
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    st.subheader("Preview Data")
    st.dataframe(df.head())

    st.divider()

    # -------------------------
    # Options
    # -------------------------

    st.subheader("Options")

    use_range = st.checkbox(
        "Use Row Range",
        value=False
    )

    # Column selection
    first_column = st.selectbox(
        "Select X-Axis Column (Time / Index)",
        df.columns
    )

    y_columns = st.multiselect(
        "Select Y-Axis Column(s)",
        df.columns,
        default=[c for c in df.columns if c != first_column][:1]
    )

    # Range input
    start_row = 0
    end_row = len(df)

    if use_range:
        st.markdown("### Row Range")

        start_row = st.number_input(
            "Start Row",
            min_value=0,
            max_value=len(df)-1,
            value=0
        )

        end_row = st.number_input(
            "End Row",
            min_value=1,
            max_value=len(df),
            value=len(df)
        )

    st.divider()

    # -------------------------
    # Process Button
    # -------------------------

    if st.button("📊 Visualize"):

        data = df.copy()

        # Apply range
        if use_range:
            data = data.iloc[start_row:end_row]

        # Extract x
        x = data[first_column]

        st.subheader("Visualization")

        # Plot
        fig, ax = plt.subplots()

        for col in y_columns:
            ax.plot(x, data[col], label=col)

        ax.set_xlabel(first_column)
        ax.set_ylabel("Value")
        ax.set_title("Time-Series Plot")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # -------------------------
        # Statistics
        # -------------------------

        st.subheader("Basic Statistics")

        stats = []

        for col in y_columns:

            series = data[col]

            stats.append({
                "Column": col,
                "Max": series.max(),
                "Min": series.min(),
                "Mean": series.mean()
            })

        stats_df = pd.DataFrame(stats)

        st.table(stats_df)


else:
    st.info("Please upload a CSV file to begin.")
