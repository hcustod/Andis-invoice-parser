import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def ocr_img(img_path):
    image = Image.open(img_path)
    text = pytesseract.image_to_string(img_path)
    return text


