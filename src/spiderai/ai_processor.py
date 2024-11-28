import os
import google.generativeai as genai
import json
from absl import logging

def process_with_ai(text_content, schema, api_key):
    """Process text content using Gemini AI to extract structured data."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""Given the following text content, extract information according to this schema:
{json.dumps(schema, indent=2)}

The response must be a valid JSON object matching the schema types.
If a field cannot be found, use null for its value.

Text content:
{text_content}

Respond only with the JSON object, no additional text."""

    try:
        response = model.generate_content(prompt)
        
        # Extract the JSON string from the response text
        response_text = response.text
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_string = response_text[json_start:json_end]
        
        # Parse the extracted JSON string
        result = json.loads(json_string)
        return result
    except Exception as e:
        raise Exception(f"Failed to process data: {str(e)}")