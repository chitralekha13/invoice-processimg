from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

def get_kernel():
    kernel = Kernel()
    kernel.add_chat_service("openai", OpenAIChatCompletion(
        service_id="openai",
        api_key="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",  
        model="gpt-4"
    ))
    kernel.import_semantic_skill_from_python("skills", "ocr_skill", "ocr_agent")
    kernel.import_semantic_skill_from_python("skills", "field_classifier_skill", "classifier_agent")
    kernel.import_semantic_skill_from_python("skills", "approval_skill", "approval_agent")
    return kernel
