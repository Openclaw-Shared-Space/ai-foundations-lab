users_database = [
    {"id": 101, "name": "Alice", "role": "admin", "is_active": True},
    {"id": 102, "name": "Bob", "role": "user", "is_active": False},
    {"id": 103, "name": "Charlie", "role": "editor", "is_active": True}
]
active_users = [user["name"] for user in users_database if user["is_active"]]
print(f"System Log: Found {len(active_users)} active users.\n")

context_block = ""
for index, name in enumerate(active_users, start=1):
    context_block += f"{index}. {name}\n"

system_prompt = f"""
You are a helpful assistant. Use the context below to answer the question.

Context:
{context_block}

Thank you!
"""
print(system_prompt)

def execute_mock_llm_call(prompt_text, model_engine="gpt-4", **kwargs):
    print(f"Routing request to target model: {model_engine}")
    print(f"Applying dynamic configuration parameters: {kwargs}")
    print("Awaiting API response...\n")
    return f"Mock API Output: Welcome aboard, {', '.join(active_users)}! Let's get to work."

if __name__ == "__main__":
    api_response = execute_mock_llm_call(
        prompt_text=system_prompt,
        model_engine="gpt-4-turbo",
        temperature=0.4,       # OpenAI specific
        max_tokens=250,        # Standard sizing
        top_k=50               # Anthropic specific (caught perfectly by **kwargs)
    )
