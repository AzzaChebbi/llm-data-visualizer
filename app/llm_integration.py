import os
import anthropic
import logging
import pandas as pd
import re
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize Anthropic client
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("Anthropic API key not found in .env file.")

client = anthropic.Anthropic(api_key=API_KEY)

def extract_visualizations(response_text):
    """
    Extracts both the visualization code and its interpretation from the LLM response.
    """
    viz_pattern = re.findall(r"```python\n(.*?)\n```", response_text, re.DOTALL)
    interp_pattern = re.findall(r"# Interpretation:(.*)", response_text)

    visualizations = []
    for i in range(len(viz_pattern)):
        visualizations.append({
            "code": viz_pattern[i].strip(),
            "interpretation": interp_pattern[i].strip() if i < len(interp_pattern) else "Pas d'interprétation disponible."
        })

    return visualizations

def preprocess_dataset(data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and filters the dataset to avoid issues in visualization.
    - Removes columns that are empty or contain only one unique value.
    - Tries to convert object columns to numeric if possible.
    """
    # Drop completely empty columns
    data = data.dropna(axis=1, how="all")

    # Drop columns with a single unique value (constant columns)
    for col in data.columns:
        if data[col].nunique() == 1:
            data = data.drop(columns=[col])

    # Convert object columns to numeric if possible
    for col in data.select_dtypes(include=["object"]).columns:
        try:
            data[col] = pd.to_numeric(data[col], errors="coerce")
        except Exception:
            pass  # Keep as object if conversion fails

    return data

def call_llm_for_viz(data: pd.DataFrame, user_request: str) -> list:
    """
    Calls the LLM to generate multiple Python visualization codes along with interpretations.
    """
    data = preprocess_dataset(data)  # Clean dataset before passing it to LLM

    if data.empty:
        return [{"code": "# Error: The dataset is empty or has no usable columns.", 
                 "interpretation": "Le dataset fourni est vide ou ne contient pas de colonnes utilisables."}]

    # Convert datetime columns to numeric for summary statistics
    for col in data.select_dtypes(include=["datetime64"]).columns:
        data[col] = data[col].astype("int64")  # Convert datetime to timestamp

    dataset_info = f"""
    Column Names and Types:
    {data.dtypes.to_string()}

    Dataset Description:
    {data.describe(include='all').to_string()}
    """

    llm_prompt = f"""
    You are an expert in Python data visualization. Given the dataset structure below, generate multiple optimal 
    visualizations using `matplotlib`, `seaborn`, or `plotly` based on the user request.

    **Dataset Overview:**
    {dataset_info}

    **User Request:**
    {user_request}

    **Instructions:**
    - Provide **at least 10 different** executable Python code snippets.
    - If possible, generate **even more** to ensure full exploration of the dataset.
    - Each snippet must include an **interpretation** explaining what the visualization represents.
    - Use `df` as the dataset (already loaded).
    - Output must follow this structure:
    
    ```python
    import matplotlib.pyplot as plt
    df["Age"].hist()
    plt.show()
    # Interpretation: This histogram shows the distribution of ages in the dataset.
    ```

    ```python
    import seaborn as sns
    sns.boxplot(x=df["Age"])
    plt.show()
    # Interpretation: This boxplot displays the spread and outliers in the Age column.
    ```
    
    **Output Requirements:**
    - **Return only Python code and interpretations** formatted exactly as shown.
    - No additional text, explanations, or markdown formatting outside the code blocks.
    - Ensure all visualizations are diverse and explore different aspects of the dataset.
    """

    logger.info("Calling LLM for visualization generation")

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,  # Increase token limit
        messages=[{"role": "user", "content": llm_prompt}]
    )

    return extract_visualizations(response.content[0].text)

