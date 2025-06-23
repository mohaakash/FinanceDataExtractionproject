import streamlit as st
import io
from pdf_processor import extract_text_from_pdf
from data_extractor import extract_financial_data


# Set up the Streamlit page
st.set_page_config(page_title="Financial Data Extractor", layout="wide")
st.title("📄 Financial Document Extractor")
st.write("Upload a PDF of a financial report, and this tool will extract key information using Google's Gemini AI.")


def is_financial_document(text: str) -> bool:
    """
    A simple heuristic to check if the text seems to be from a financial document
    by looking for common financial keywords.
    """
    # A list of common, case-insensitive keywords
    keywords = ["revenue", "net income", "profit", "loss", "ebitda",
                "assets", "liabilities", "equity", "cash flow", "financial statement"]
    lower_text = text.lower()
    # Check if at least two distinct keywords are present
    found_keywords = sum(1 for keyword in keywords if keyword in lower_text)
    return found_keywords >= 2


# --- API Test Section ---
st.subheader("API Connection Test")
st.write("Click the button below to test the connection to the Gemini API with sample data, bypassing the PDF upload.")

if st.button("Test Gemini API Connection"):
    # Sample text that mimics a financial report snippet
    sample_text = """
    In the fourth quarter, TechCorp Inc. (NASDAQ: TCORP) reported record revenue of 5.2 billion dollars.
    The company's net income for the period was 1.1 billion dollars.
    """
    with st.spinner("Testing API..."):
        st.info("Sending sample text to Gemini API...")
        test_data = extract_financial_data(sample_text)
        st.success("✅ API test complete.")
        st.write("API Response:")
        st.json(test_data)

st.divider()

st.subheader("Upload Your Document")

# File uploader widget
uploaded_file = st.file_uploader(
    "Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    pdf_buffer = io.BytesIO(bytes_data)

    st.info("File uploaded successfully. Processing...")

    # --- Step 1: Extract text from PDF ---
    with st.spinner("Step 1/2: Extracting text from PDF..."):
        extracted_text = extract_text_from_pdf(pdf_buffer)

    if not extracted_text:
        st.error(
            "Could not extract text from the PDF. The file might be empty, corrupted, or contain only images.")
    else:
        st.success("✅ Text extracted successfully.")

        # --- Preliminary check if the document seems relevant ---
        if not is_financial_document(extracted_text):
            st.warning(
                "⚠️ This document does not seem to be a financial report. Analysis will proceed, but results may be inaccurate.")

        # --- Step 2: Extract financial data using Gemini ---
        with st.spinner("Step 2/2: Analyzing text with Gemini AI..."):
            financial_data = extract_financial_data(extracted_text)

        st.success("✅ Analysis complete.")

        if "error" in financial_data:
            st.error(f"An error occurred: {financial_data['error']}")
        elif "result" in financial_data:
            st.subheader("Extracted Financial Data")
            st.text(financial_data["result"])
        else:
            st.warning("No specific financial data was found in the document.")

        # Optionally, show the full extracted text in an expander
        with st.expander("View Full Extracted Text"):
            st.text_area("Extracted Text", extracted_text,
                         height=300, label_visibility="collapsed")
