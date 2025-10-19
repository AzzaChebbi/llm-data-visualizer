# 🔍 AI-Powered Data Visualization

Intelligent data visualization generator using Claude AI to automatically create insightful charts and graphs from your CSV datasets. Simply describe what you want to see, and let AI generate multiple visualizations with explanations.

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Claude AI](https://img.shields.io/badge/Claude-3.5%20Sonnet-purple.svg)](https://www.anthropic.com/claude)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 Overview

This project leverages Claude AI (Anthropic) to automatically generate Python visualization code based on natural language requests. Upload a CSV file, describe what insights you want, and watch as the AI creates multiple diverse visualizations with detailed interpretations.

## ✨ Features

- 🤖 **AI-Powered Generation**: Uses Claude 3.5 Sonnet to create visualization code
- 📊 **Multiple Visualizations**: Generates 10+ different charts per request
- 🧠 **Smart Analysis**: Automatically analyzes dataset structure and suggests optimal visualizations
- 📝 **Auto Interpretations**: Each chart comes with AI-generated explanations
- 🔄 **Data Preprocessing**: Automatic cleaning and type conversion
- 🎨 **Multiple Libraries**: Supports matplotlib, seaborn, and plotly
- ⚡ **Interactive UI**: Built with Streamlit for easy interaction
- 🧪 **Tested**: Comprehensive test suite with pytest

## 📋 Table of Contents

1. [Demo](#-Demo)
2. [Architecture](#-architecture)
3. [Installation](#-installation)
4. [Usage](#-usage)
5. [Project Structure](#-project-structure)
6. [Testing](#-testing)
7. [Configuration](#-configuration)
8. [Examples](#-examples)
9. [License](#-license)
10. [Future Enhancements](#-future-enhancements)

## 🎬 Demo

**Example Request:** "Show me the distribution of ages and their correlation with salary"

**AI Generates:**
1. Age distribution histogram
2. Salary boxplot
3. Age vs Salary scatter plot
4. Correlation heatmap
5. Violin plots
6. Pair plots
7. And more...

Each with detailed interpretations!

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │ (main.py)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ User Upload CSV │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Preprocessing  │ (llm_integration.py)
│  - Clean data   │
│  - Type convert │
│  - Remove empty │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Claude API    │ (llm_integration.py)
│  Generate Viz   │
│  + Interpret    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Execute Code   │ (main.py)
│  Display Charts │
└─────────────────┘
```

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-data-visualization.git
cd ai-data-visualization
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the app directory:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## 🚀 Usage

### Running the Application

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

### Step-by-Step Guide

1. **Upload CSV File**
   - Click "📂 Upload a CSV file"
   - Select your dataset (must be .csv format)

2. **Preview Your Data**
   - View the first few rows automatically displayed

3. **Describe Your Request**
   - Enter natural language request like:
     - "Show distribution of all numerical columns"
     - "Compare sales across different regions"
     - "Visualize correlations between features"
     - "Create a time series plot of revenue"

4. **Generate Visualizations**
   - Click "🚀 Generate Visualizations"
   - Wait for AI to analyze and generate charts
   - View multiple visualizations with interpretations

### Example Requests

```
"Show me histograms for all numerical columns"
"Create a correlation heatmap"
"Visualize the distribution of Age and its relationship with Salary"
"Plot time series trends"
"Compare categories with bar charts"
"Show outliers using box plots"
```

## 📁 Project Structure

```
├── main.py                     # Streamlit app and visualization executor
├── llm_integration.py          # Claude API integration and preprocessing
├── helpers.py                  # Utility functions for data analysis
├── test_app.py                 # Pytest test suite
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

### File Descriptions

#### `main.py`
- Streamlit UI implementation
- File upload handling
- Visualization execution
- Display management

#### `llm_integration.py`
- Claude API client initialization
- Data preprocessing pipeline
- Prompt engineering for visualization generation
- Response parsing and code extraction

#### `helpers.py`
- Column name extraction from natural language
- Summary statistics generation
- Correlation heatmap creation
- Data quality checks

#### `test_app.py`
- Unit tests for all components
- Mock API responses
- Code extraction tests
- Visualization execution tests


## 🧪 Testing

Run the test suite:

```bash
pytest test_llm.py -v
```

### Test Coverage

- LLM API integration
- Code extraction from responses
- Data preprocessing
- Helper functions
- Visualization execution
- Error handling

## ⚙️ Configuration

### Adjusting AI Behavior

Edit `llm_integration.py`:

```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",  # Claude model
    max_tokens=4096,                      # Response length
    temperature=0.7,                      # Creativity (0-1)
    messages=[{"role": "user", "content": llm_prompt}]
)
```

### Visualization Library Preferences

Modify the prompt in `call_llm_for_viz()` to prefer:
- **matplotlib** - Traditional, publication-ready
- **seaborn** - Statistical visualizations
- **plotly** - Interactive charts

### Number of Visualizations

Change in the prompt:
```python
"Provide **at least 10 different** executable Python code snippets."
```

## 📊 Examples

<p align="center">
  <img src="https://github.com/user-attachments/assets/66f91b4a-107d-48c2-aa9e-917fdeef45ba" alt="exemple" width="309" height="676">
</p>

<img width="1909" height="946" alt="graphe1" src="https://github.com/user-attachments/assets/6f4f6876-d699-4e94-80a6-7a9f4d050d70" />

<p align="center">
<img width="325" height="650" alt="graphe2" src="https://github.com/user-attachments/assets/21486c74-57a3-46b7-aaf9-fdee054a9ecf" />
</p>

<p align="center">
<img width="306" height="892" alt="graphe3" src="https://github.com/user-attachments/assets/610e55b6-55ee-45f0-998b-519a6b4bc28c" />
</p>

<p align="center">
<img width="312" height="759" alt="graphe4" src="https://github.com/user-attachments/assets/4acc49fe-3100-472a-b2e2-c9eb32e21b51" />
</p>

## 🛠️ Advanced Features

### Error Handling

The system handles:
- Empty datasets
- Invalid column types
- Missing values
- Malformed code
- API errors

## 📄 License

This project is licensed under the MIT License 

## ✨ Future Enhancements

- [ ] Support for Excel files
- [ ] Real-time data streaming
- [ ] Custom theme support
- [ ] Multi-language support
- [ ] Interactive dashboard builder
- [ ] PDF report generation
- [ ] API endpoint for programmatic access

---

**Made with ❤️ and AI | Powered by Claude, Streamlit, and Python**
