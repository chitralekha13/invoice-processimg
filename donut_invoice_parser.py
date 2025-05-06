from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch
import pandas as pd
import os
import json

# ✅ Use invoice-focused SROIE model
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def parse_invoice(image_path):
    image = Image.open(image_path).convert("RGB")

    task_prompt = "<s>" + processor.tokenizer.eos_token  # ✅ use simpler prompt
    pixel_values = processor(image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    generated_ids = model.generate(
        pixel_values,
        max_length=512,
        num_beams=3,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
    )

    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

    # ✅ Attempt to convert to JSON
    try:
        data = json.loads(generated_text)
    except json.JSONDecodeError:
        print("⚠️ JSON parsing failed. Output returned as raw text.")
        data = {"raw_output": generated_text}

    return data

def save_structured_output(data, output_path="output/structured_data.csv"):
    os.makedirs("output", exist_ok=True)

    if "raw_output" in data:
        print("⚠️ Could not parse structured fields. Raw text output was returned.")
        with open("output/raw_output.txt", "w", encoding="utf-8") as f:
            f.write(data["raw_output"])
        return

    df = pd.DataFrame([data])
    df.to_csv(output_path, index=False)
    print(f"✅ Structured output saved to: {output_path}")

# Run script
if __name__ == "__main__":
    invoice_path = "data/invoices/invoice3.webp"
    result = parse_invoice(invoice_path)
    print("🔍 Extracted Data:\n", result)
    save_structured_output(result)
