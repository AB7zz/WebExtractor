# SpiderAI

A Python library for extracting structured data from web pages using AI. This library uses Google's Gemini AI to intelligently extract and format data according to your specified schema.

## Features

- AI-powered content analysis using Google's Gemini AI
- Flexible schema definition for structured data extraction
- Automatic handling of web page fetching and parsing
- Supports both single objects and arrays of objects

## Installation

```bash
pip install spiderai
```

## Quick Start

1. First, get your Gemini AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Create a `.env` file in your project root and add your API key:

```
GEMINI_API_KEY=your_api_key_here
```

3. Use the library in your code:

```python
from spiderai import WebDataExtractor
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Create the extractor
extractor = WebDataExtractor(api_key=gemini_api_key)

# URL to extract data from
url = "https://yoururl.com"

# Define your schema
schema = {
    "key1": "string",
    "key2": "float",
    "key3": "string"
}

# Extract the data
result = extractor.extract(url, schema)

# Use the extracted data
print("Product Name:", result["key1"])
print("Price:", result["key2"])
print("Description:", result["key3"])
```

## Schema Definition

The schema is a dictionary where:
- Keys are the field names you want to extract
- Values are the expected data types ("string", "float", "integer", "boolean", "number", None)

Example schema:

```python
# Product schema
schema = {
    "name": "string",
    "price": "float",
    "rating": "float",
    "review_count": "integer"
}

# Array of objects
schema = [
    {
        "name": "string",
        "price": "float"
    }
]
```

## Requirements

- Python 3.10 or higher
- Google Gemini AI API key
- Internet connection for web scraping and AI processing


## License

This project is licensed under MIT License

## Contact

Feel free to contribute to the project by opening issues or suggesting improvements. For any queries, you can reach me at abhinavcv007@gmail.com