import fitz
import re
import sys
import argparse

def parse_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text


def extract_keywords(text, keywords):
    extracted_data = {}
    patterns = {
        "Invoice number": re.compile(r"Invoice number[:\s]*([0-9A-Za-z-]+)", re.IGNORECASE),
        "Invoice date": re.compile(r"([A-Za-z0-9, ]+)\s*Invoice date", re.IGNORECASE),
        "Subtotal in CAD": re.compile(r"([0-9,]+\.\d{2})\s*Subtotal in CAD", re.IGNORECASE),
        "Total in CAD": re.compile(r"([0-9,]+\.\d{2})\s*Total in CAD", re.IGNORECASE),
    }

    for keyword, pattern in patterns.items():
        match = pattern.search(text)
        if match:
            extracted_data[keyword] = match.group(1).strip()
    return extracted_data


def main():
    parser = argparse.ArgumentParser(description="Extract keywords from PDF invoices.")
    parser.add_argument("pdf_path", help="Path to the PDF file.")
    parser.add_argument("--debug", action="store_true", help="Print raw text extracted from the PDF for debugging.")
    args = parser.parse_args()

    text = parse_pdf(args.pdf_path)

    if args.debug:
        print("Raw Text Extracred from PDF:")
        print(text) 
        print("\n")

    keywords = ["Invoice number", "Invoice date", "Subtotal in CAD", "Total in CAD"]
    extracted_data = extract_keywords(text, keywords)
    
    print("Extracted Keywords and Values:")
    for key, value in extracted_data.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
