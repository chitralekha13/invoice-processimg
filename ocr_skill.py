import pytesseract
from PIL import Image

def extract_text(sk_context):
    image_path = sk_context["image_path"]
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        sk_context["raw_text"] = text
        return sk_context
    except Exception as e:
        sk_context["raw_text"] = ""
        return sk_context
