

#pip install streamlit pdf2image pillow pytesseract

#Taking more time for hand written text 

import streamlit as st
from pdf2image import convert_from_bytes, convert_from_path
from PIL import Image, ImageDraw
import pytesseract
import os

# Optional: Set tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# Streamlit UI config
st.set_page_config(page_title="Scanned PDF Text Search", layout="wide")
st.title("🔍 Search & Highlight in Scanned PDF")

# PDF path on your system
uploaded_pdf_path = r"C:\Users\Srilatha\Downloads\scanned1.pdf"
# Try loading the PDF
if not os.path.exists(uploaded_pdf_path):
    st.error(f"❌ PDF file not found at path:\n`{uploaded_pdf_path}`")
else:
    try:
        with open(uploaded_pdf_path, "rb") as f:
            pdf_data = f.read()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        pdf_data = None

    search_term = st.text_input("Enter text to search (case-insensitive, multiple words separated by space)", placeholder="e.g., report value formula")

    if pdf_data and search_term.strip():
        search_terms = [term.strip().lower() for term in search_term.strip().split()]
        st.info("Processing PDF... This may take a moment ⏳")

        images = convert_from_path(
            uploaded_pdf_path,
            poppler_path=r"C:\Users\Srilatha\poppler-24.08.0\Library\bin"
        )
        found_any = False

        for page_num, image in enumerate(images):
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            draw = ImageDraw.Draw(image, "RGBA")
            matches = 0

            for i, word in enumerate(ocr_data['text']):
                word_text = word.strip()
                if word_text:
                    word_lower = word_text.lower()
                    for term in search_terms:
                        if term in word_lower:
                            x, y, w, h = (ocr_data['left'][i], ocr_data['top'][i],
                                          ocr_data['width'][i], ocr_data['height'][i])
                            draw.rectangle([x, y, x + w, y + h], fill=(255, 0, 0, 80), outline="red", width=2)
                            matches += 1
                            break  # Avoid multiple matches on the same word

            if matches > 0:
                found_any = True
                st.image(image, caption=f"✅ Page {page_num + 1}: {matches} match(es) found", use_column_width=True)
            else:
                st.markdown(f"<p style='color: gray;'>❌ Page {page_num + 1}: No matches found</p>", unsafe_allow_html=True)

        if not found_any:
            st.warning("No matching text found in the entire scanned PDF.")

    elif pdf_data and not search_term:
        st.info("Please enter text to search in the box above.")
