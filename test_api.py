from prompts import get_system_prompt
from services.llm_service import generate_response


mode = "AI Tutor"

system_prompt = get_system_prompt(mode)

user_prompt = "What is machine learning?"

response = generate_response(
    system_prompt,
    user_prompt
)

print("MODE:", mode)
print()
print(response)