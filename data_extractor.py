from google import genai
from google.genai import types
import streamlit as st
from typing import Dict, Union
from config import get_google_api_key

# Configuration constants
PROMPT_TEMPLATE = """You are a financial data extraction assistant. Extract these details if explicitly mentioned:
- Company Name
- Stock Symbol
- Revenue
- Net Income

Return the information as plain text, one item per line. If something is missing, write "Not found" for that item.

Text to analyze:

{text}
---"""


class FinancialDataExtractor:
    def __init__(self):
        """Initialize the Gemini API client."""
        self.client = None
        self.initialize_client()

    def initialize_client(self):
        """Initialize the Gemini API client with configuration."""
        try:
            api_key = get_google_api_key()
            if api_key:
                self.client = genai.Client(api_key=api_key)
                st.success("✅ Gemini API client initialized successfully")
            else:
                st.error("❌ No API key found")
        except Exception as e:
            st.error(f"❌ Failed to initialize Gemini client: {str(e)}")

    def extract_data(self, text: str) -> Dict[str, Union[str, float, None]]:
        """Extract financial data from text using Gemini API."""
        if not self.client:
            return {"error": "API client not initialized"}

        if not text or not text.strip():
            return {"error": "Empty input text"}

        try:
            prompt = PROMPT_TEMPLATE.format(text=text)
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config=self._get_generation_config()
            )
            return self._process_response(response)

        except Exception as e:
            return {"error": f"API Error: {str(e)}"}

    def _get_generation_config(self) -> types.GenerateContentConfig:
        """Return the configuration for content generation."""
        return types.GenerateContentConfig(
            response_mime_type="text/plain",
            # thinking_config=types.ThinkingConfig(thinking_budget=0),
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"},
            ]
        )

    def _process_response(self, response) -> Dict[str, str]:
        """Process the API response and return plain text."""
        try:
            response_text = getattr(response, 'text', '')
            if not response_text and hasattr(response, 'candidates'):
                if response.candidates and hasattr(response.candidates[0].content, 'parts'):
                    response_text = response.candidates[0].content.parts[0].text

            if not response_text:
                return {"error": "Empty API response"}

            st.info(f"Raw API Response: {response_text}")

            # Just return the plain text
            return {"result": response_text.strip()}

        except Exception as e:
            return {"error": f"Response processing error: {str(e)}"}


# ✅ Wrapper function for easy use
def extract_financial_data(text: str) -> Dict[str, Union[str, float, None]]:
    extractor = FinancialDataExtractor()
    return extractor.extract_data(text)
