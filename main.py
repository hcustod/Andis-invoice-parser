import fitz
import re
import sys

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
        "Invoice number": re.compile(r"Invoice number:?\s*([0-9A-Za-z-]+)", re.IGNORECASE),
        "Invoice date": re.compile(r"Invoice date:?\s*([A-Za-z0-9, ]+)", re.IGNORECASE),
        "Subtotal in CAD": re.compile(r"Subtotal in CAD:?\s*([\d,]+\.\d{2})", re.IGNORECASE),
        "Total in CAD": re.compile(r"Total in CAD:?\s*([\d,]+\.\d{2})", re.IGNORECASE),
    }

    for keyword, pattern in patterns.items():
        match = pattern.search(text)
        if match:
            extracted_data[keyword] = match.group(1).strip()
    return extracted_data


def main():
    if len(sys.argv) != 2:
        print("Usage: python invoice_parser.py <pdf_path>")
        return

    pdf_path = sys.argv[1]
    keywords = ["Invoice number", "Invoice date", "Subtotal in CAD", "Total in CAD"]
    text = parse_pdf(pdf_path)
    extracted_data = extract_keywords(text, keywords)
    
    print("Extracted Keywords and Values:")
    for key, value in extracted_data.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
