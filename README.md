# AI Text Summarizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

A powerful text summarization tool that provides both extractive and abstractive summarization capabilities through an intuitive web interface and REST API.

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [How It Works](#-how-it-works)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## ✨ Features

- **Dual Summarization Methods**:
  - **Extractive**: Implements the TextRank algorithm to identify and extract key sentences
  - **Abstractive**: Uses frequency analysis with coherence enhancement for more natural summaries
- **Adjustable Summary Length**: Control the conciseness of your summaries
- **Modern Web Interface**: Clean, responsive design built with Bootstrap
- **REST API**: Programmatic access for integration with other applications
- **Fast Processing**: Efficient algorithms for quick summarization

## 🎬 Demo

### Screenshots

*Screenshots of the application will be added here after deployment.*

### Video Demo

*A video demonstration of the application will be added here after deployment.*

## 📁 Project Structure

```
text-summarizer/
├── app.py              # Flask application
├── models/             # Model handling
│   ├── __init__.py
│   ├── extractive.py   # Extractive summarization
│   └── abstractive.py  # Abstractive summarization
├── static/             # Static files
│   ├── css/            # CSS files
│   │   └── style.css   # Custom styles
│   └── js/             # JavaScript files
│       └── main.js     # Custom scripts
├── templates/          # HTML templates
│   ├── index.html      # Main page
│   └── layout.html     # Base template
├── test_summarizers.py # Test script for summarizers
└── requirements.txt    # Dependencies
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/ShahdMohamed10/Text-Summarizer.git
cd Text-Summarizer
```

2. **Create and activate a virtual environment**

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
python app.py
```

The application will be available at http://127.0.0.1:5000/

## 💻 Usage

### Web Interface

1. Open your web browser and navigate to http://127.0.0.1:5000/
2. Enter or paste the text you want to summarize in the text area
3. Choose the summarization method (extractive, abstractive, or both)
4. Adjust the summary length using the slider
5. Click the "Summarize" button
6. View the results in the tabs below

### Testing the Summarizers

You can test the summarization functionality using the included test script:

```bash
python test_summarizers.py
```

## 🔌 API Documentation

The application provides a RESTful API endpoint for summarization:

### Endpoint: `/summarize`

**Method**: POST

**Content-Type**: application/json

**Request Body**:

```json
{
  "text": "Your text to summarize...",
  "method": "both",  // "extractive", "abstractive", or "both"
  "ratio": 0.3       // Proportion of original text to keep (0.1-0.5)
}
```

**Response**:

```json
{
  "extractive": "Extractive summary...",
  "abstractive": "Abstractive summary..."
}
```

**Example using curl**:

```bash
curl -X POST http://localhost:5000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"Your text here...","method":"both","ratio":0.3}'
```

**Example using Python requests**:

```python
import requests
import json

url = "http://localhost:5000/summarize"
data = {
    "text": "Your text here...",
    "method": "both",
    "ratio": 0.3
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), indent=2))
```

## 🧠 How It Works

### Extractive Summarizer

The extractive summarizer works by:

1. Breaking the text into sentences
2. Creating a similarity matrix between sentences
3. Using the TextRank algorithm (similar to PageRank) to score sentences
4. Applying position-based weighting to favor important positions
5. Ensuring diversity in the selected sentences
6. Selecting the top-scoring sentences based on the specified ratio
7. Reordering the selected sentences to match their original order

### Abstractive Summarizer

The abstractive summarizer works by:

1. Breaking the text into sentences
2. Calculating word frequencies in the text
3. Scoring sentences based on the frequency of their words
4. Applying position-based weighting
5. Selecting the top-scoring sentences based on the specified ratio
6. Enhancing coherence by adding appropriate transition words

## 🔮 Future Improvements

- Multi-language support
- Advanced summarization algorithms
- Summary quality evaluation metrics
- URL and file upload support
- User accounts and saved summaries
- Batch processing capabilities

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📬 Contact

Shahd Mohamed - [LinkedIn](https://www.linkedin.com/in/shahd-mohamed-123a68277/) - [GitHub](https://github.com/ShahdMohamed10)

Project Link: [https://github.com/ShahdMohamed10/Text-Summarizer](https://github.com/ShahdMohamed10/Text-Summarizer) 