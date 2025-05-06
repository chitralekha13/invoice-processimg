from semantic_kernel.kernel import Kernel
from kernel_config import get_kernel

def run_invoice_pipeline(image_path):
    kernel = get_kernel()
    context = kernel.create_new_context()
    context["image_path"] = image_path
    print("📌 Running OCR agent...")
    context = kernel.run_sync("ocr_agent", "extract_text", input_vars=context.variables)
    print("📌 Running classifier agent...")
    context = kernel.run_sync("classifier_agent", "classify_fields", input_vars=context.variables)
    print("📌 Running approval agent...")
    context = kernel.run_sync("approval_agent", "route_for_approval", input_vars=context.variables)
    return context["approval_result"]
