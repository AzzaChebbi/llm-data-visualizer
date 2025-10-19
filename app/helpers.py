import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import re

def extract_column_from_answer(answer):
    """
    Extracts a column name from the user request.
    """
    match = re.search(r"(?:visualize|plot|show)\s*the\s*(\w+)", answer, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def summary_statistics(dataset):
    """
    Returns summary statistics of the dataset, avoiding errors on bad columns.
    """
    if dataset.empty:
        return "Dataset is empty or has no usable columns."

    return dataset.describe(include='all', datetime_is_numeric=True)

def correlation_heatmap(dataset):
    """
    Generates a correlation heatmap, ensuring there are enough numerical columns.
    """
    numerical_cols = dataset.select_dtypes(include=["number"])

    if numerical_cols.shape[1] < 2:
        st.write("Not enough numerical columns to generate a heatmap.")
        return

    plt.figure(figsize=(10, 8))
    sns.heatmap(numerical_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    st.pyplot()