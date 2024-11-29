import os
import google.generativeai as genai
import json
from absl import logging

def validate_schema(schema):
    """Validate the schema structure."""
    if isinstance(schema, dict):
        # Single item schema validation
        for key, value in schema.items():
            if not isinstance(key, str):
                raise ValueError("Schema keys must be strings")
            if value not in ['string', 'integer', 'number', 'boolean', 'array', 'float', None]:
                raise ValueError(f"Invalid type in schema: {value}")
    elif isinstance(schema, list) and len(schema) == 1:
        # Array schema validation - should contain exactly one dict
        validate_schema(schema[0])
    else:
        raise ValueError("Schema must be either a dictionary or a single-item list containing a dictionary")

def process_with_ai(text_content, schema, api_key):
    validate_schema(schema)
    """Process text content using Gemini AI to extract structured data."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    is_array = isinstance(schema, list)
    schema_dict = schema[0] if is_array else schema

    prompt = f"""Given the following text content, extract information according to this schema:
{json.dumps(schema_dict, indent=2)}

The response must be a valid JSON {'array of objects' if is_array else 'object'} matching the schema types.
{'Each object in the array should follow the schema structure.' if is_array else ''}
If a field cannot be found, use null for its value.

Text content:
{text_content}

Respond only with the JSON {'array' if is_array else 'object'}, no additional text."""

    try:
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Handle both array and object responses
        if is_array:
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
        else:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
        json_string = response_text[json_start:json_end]
        result = json.loads(json_string)
        return result
    except Exception as e:
        raise Exception(f"Failed to process data: {str(e)}")