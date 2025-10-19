

import pytest
import pandas as pd
import re
from llm_integration import call_llm_for_viz, clean_llm_code
from helpers import extract_column_from_answer, summary_statistics
from main import execute_viz_code
import matplotlib.pyplot as plt
import seaborn as sns

# Mock DataFrame for testing
TEST_DF = pd.DataFrame({
    "Age": [25, 30, 35, 40, 45],
    "Salary": [50000, 60000, 70000, 80000, 90000]
})

### Test LLM Integration ###
def test_call_llm_for_viz(mocker):
    """Ensure call_llm_for_viz() returns valid visualization code."""
    mock_response = "```python\nimport matplotlib.pyplot as plt\ndf['Age'].hist()\nplt.show()\n```"
    
    # Mock LLM response
    mocker.patch("llm_integration.client.messages.create", return_value=mocker.Mock(content=[mocker.Mock(text=mock_response)]))
    
    result = call_llm_for_viz(TEST_DF, "Show histogram of Age")
    assert len(result) > 0
    assert "df['Age'].hist()" in result[0]  # Check if expected code snippet is returned

### Test Code Extraction ###
def test_clean_llm_code():
    """Ensure clean_llm_code() extracts Python code correctly."""
    response_text = """
    Here is your code:
    ```python
    import matplotlib.pyplot as plt
    df['Age'].hist()
    plt.show()
    ```
    """
    extracted_code = clean_llm_code(response_text)
    assert len(extracted_code) > 0
    assert "df['Age'].hist()" in extracted_code[0]

### Test Helpers ###
def test_extract_column_from_answer():
    """Test extracting a column name from a user's request."""
    assert extract_column_from_answer("Show a bar chart of Age") == "Age"
    assert extract_column_from_answer("Visualize the Salary distribution") == "Salary"
    assert extract_column_from_answer("Plot histogram") is None  # No specific column

def test_summary_statistics():
    """Check if summary_statistics() returns valid descriptive stats."""
    stats = summary_statistics(TEST_DF)
    assert "Age" in stats.columns
    assert "Salary" in stats.columns
    assert not stats.empty

### Test Visualization Execution ###
def test_execute_viz_code(mocker):
    """Test executing visualization code to ensure it does not raise errors."""
    viz_code = "import matplotlib.pyplot as plt\ndf['Age'].hist()\nplt.show()"
    
    # Mock Streamlit functions
    mock_st = mocker.Mock()
    mock_st.pyplot = mocker.Mock()

    try:
        execute_viz_code([viz_code], TEST_DF)
        assert True  # If no exception, test passes
    except Exception as e:
        pytest.fail(f"Visualization execution failed with error: {e}")