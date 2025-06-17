

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
#uploaded_pdf_path = r"C:\Users\Srilatha\Downloads\seeds.pdf"
uploaded_pdf_path = r"C:\Users\Srilatha\Downloads\scanned1.pdf"
#uploaded_pdf_path = r"C:\Users\Srilatha\Downloads\ammu_doc.pdf"
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

    # Ask user for search term
    search_term = st.text_input("Enter text to search (case-insensitive)", placeholder="e.g., report, value, formula")

    if pdf_data and search_term.strip():
        search_term = search_term.strip()
        st.info("Processing PDF... This may take a moment ⏳")

        #images = convert_from_bytes(pdf_data, poppler_path=r"C:\Users\Srilatha\poppler-24.08.0\Library\bin")
        images = convert_from_path(r"C:\Users\Srilatha\Downloads\scanned1.pdf", poppler_path=r"C:\Users\Srilatha\poppler-24.08.0\Library\bin")
        found_any = False

        for page_num, image in enumerate(images):
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            draw = ImageDraw.Draw(image, "RGBA")
            matches = 0

            for i, word in enumerate(ocr_data['text']):
                word_text = word.strip()
                if word_text and search_term.lower() in word_text.lower():
                    x, y, w, h = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
                    draw.rectangle([x, y, x + w, y + h], fill=(255, 0, 0, 80), outline="red", width=2)
                    matches += 1

            if matches > 0:
                found_any = True
                st.image(image, caption=f"✅ Page {page_num + 1}: {matches} match(es) found", use_column_width=True)
            else:
                st.markdown(f"<p style='color: gray;'>❌ Page {page_num + 1}: No matches found</p>", unsafe_allow_html=True)

        if not found_any:
            st.warning("No matching text found in the entire scanned PDF.")

    elif pdf_data and not search_term:
        st.info("Please enter text to search in the box above.")
        
