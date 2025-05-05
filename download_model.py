from transformers import LayoutLMv2Processor, LayoutLMv2ForTokenClassification
import os

MODEL_NAME = "microsoft/layoutlmv2-base-uncased"
MODEL_DIR = "./model"

def download_model_and_processor():
    os.makedirs(MODEL_DIR, exist_ok=True)

    print("⬇️ Downloading processor...")
    processor = LayoutLMv2Processor.from_pretrained(MODEL_NAME)
    processor.save_pretrained(os.path.join(MODEL_DIR, "tokenizer"))

    print("⬇️ Downloading model...")
    model = LayoutLMv2ForTokenClassification.from_pretrained(MODEL_NAME)
    model.save_pretrained(MODEL_DIR)

    print("✅ Model and tokenizer saved successfully.")

if __name__ == "__main__":
    download_model_and_processor()
