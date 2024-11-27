import requests
from bs4 import BeautifulSoup
from .ai_processor import process_with_ai

class WebDataExtractor:
    def __init__(self, api_key):
        """Initialize the WebDataExtractor with Gemini AI API key."""
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key

    def extract(self, url, schema):
        """
        Extract data from a URL according to the provided schema.
        
        Args:
            url (str): The URL to extract data from
            schema (dict): Schema defining the required data and their types
        
        Returns:
            dict: Extracted data matching the schema
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract all text content from relevant tags
        text_content = ' '.join([
            tag.get_text(strip=True)
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'span', 'div', 'a'])
            if tag.get_text(strip=True)
        ])

        return process_with_ai(text_content, schema, self.api_key)