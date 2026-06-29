# test_ocr.py
import pytesseract
from PIL import Image

# Load your bill image
img = Image.open("/Users/shubham/Downloads/ai intern/Copy of WhatsApp Image 2026-02-12 at 13.48.47 (1).jpeg")

# Extract text
text = pytesseract.image_to_string(img, lang="eng+hin")

print(text)