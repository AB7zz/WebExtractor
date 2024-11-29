import requests
from bs4 import BeautifulSoup
from .ai_processor import process_with_ai
from functools import lru_cache
import time
import json

class WebDataExtractor:
    def __init__(self, api_key, rate_limit=1):
        """Initialize the WebDataExtractor with Gemini AI API key."""
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.last_request_time = 0
        self.rate_limit = rate_limit  # minimum seconds between requests

    def _make_cache_key(self, url, schema):
        """Create a hashable cache key from url and schema."""
        # Convert schema to a string representation for hashing
        schema_str = json.dumps(schema, sort_keys=True)
        return (url, schema_str)

    @lru_cache(maxsize=100)
    def _cached_extract(self, cache_key):
        """Internal cached extraction method."""
        url, schema_str = cache_key
        schema = json.loads(schema_str)
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch URL: {str(e)}")

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # More sophisticated text extraction
        text_blocks = []
        
        # Priority elements first
        for tag in soup.find_all(['h1', 'h2', 'h3']):
            text_blocks.append(f"Heading: {tag.get_text(strip=True)}")
            
        # Main content
        for tag in soup.find_all(['p', 'article', 'section']):
            text_blocks.append(tag.get_text(strip=True))
            
        # Additional content
        for tag in soup.find_all(['span', 'div']):
            if len(tag.get_text(strip=True)) > 50:  # Only substantial content
                text_blocks.append(tag.get_text(strip=True))
                
        text_content = '\n'.join(text_blocks)

        # Add rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit:
            time.sleep(self.rate_limit - time_since_last)
        
        result = process_with_ai(text_content, schema, self.api_key)
        self.last_request_time = time.time()
        return result

    def extract(self, url, schema):
        """Public extract method that handles caching."""
        cache_key = self._make_cache_key(url, schema)
        return self._cached_extract(cache_key)