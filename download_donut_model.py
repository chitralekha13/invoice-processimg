from transformers import DonutProcessor, VisionEncoderDecoderModel

MODEL_NAME = "naver-clova-ix/donut-base-finetuned-docvqa"
SAVE_PATH = "./donut-model"

processor = DonutProcessor.from_pretrained(MODEL_NAME)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)

processor.save_pretrained(SAVE_PATH)
model.save_pretrained(SAVE_PATH)

print("✅ Donut model downloaded to", SAVE_PATH)
