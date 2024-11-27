# Web Data Extractor

A Python library for extracting structured data from web pages using AI. This library uses Google's Gemini AI to intelligently extract and format data according to your specified schema.

## Features

- Easy-to-use interface for web data extraction
- AI-powered content analysis using Google's Gemini AI
- Flexible schema definition for structured data extraction
- Automatic handling of web page fetching and parsing

## Installation

```bash
pip install web_extractor
```

## Quick Start

1. First, get your Gemini AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Create a `.env` file in your project root and add your API key:

```
GEMINI_API_KEY=your_api_key_here
```

3. Use the library in your code:

```python
from web_extractor import WebDataExtractor
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Create the extractor
extractor = WebDataExtractor(api_key=gemini_api_key)

# URL to extract data from
url = "https://www.amazon.in/Celestron-AstroMaster-130-EQ-Telescope/dp/B000MLL6RS"

# Define your schema
schema = {
    "name": "string",
    "price": "float",
    "description": "string"
}

# Extract the data
result = extractor.extract(url, schema)

# Use the extracted data
print("Product Name:", result["name"])
print("Price:", result["price"])
print("Description:", result["description"])
```

## Schema Definition

The schema is a dictionary where:
- Keys are the field names you want to extract
- Values are the expected data types ("string", "float", "integer", etc.)

Example schemas:

```python
# Product schema
schema = {
    "name": "string",
    "price": "float",
    "rating": "float",
    "review_count": "integer"
}
```

## Requirements

- Python 3.10 or higher
- Google Gemini AI API key
- Internet connection for web scraping and AI processing