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


def extract_keywords(text, keywords, context_range=50):
    extracted_data = {}

    for keyword in keywords:
        pattern_before = re.compile(rf"([A-Za-z0-9, \$\.\-]{{1,{context_range}}})\s*{keyword}", re.IGNORECASE)

        match_before = pattern_before.search(text)

        if match_before:
            extracted_data[keyword] = match_before.group(1).strip()
        else:
            extracted_data[keyword] = None
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

    keywords = input("Enter keywords seperated by commas: ").split(',')
    keywords = [keyword.strip() for keyword in keywords]
    
    extracted_data = extract_keywords(text, keywords)
    
    print("Extracted Keywords and Values:")
    for key, value in extracted_data.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
