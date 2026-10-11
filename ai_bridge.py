# ai_bridge.py
from pydantic import BaseModel, ValidationError
import requests

# 1. DEFINE THE VALIDATION MODEL
# We expect the LLM to return a profile containing exactly these three fields.
# Pydantic will auto-cast types (e.g., converting string "95" to integer 95) or fail fast.
class UserInsight(BaseModel):
    user_name: str
    sentiment_score: int
    is_flagged_for_review: bool

print("Pydantic Schema enforces: user_name (str), sentiment_score (int), is_flagged_for_review (bool)\n")

# 2. CONSTRUCTING THE API CALL
def analyze_user_data_via_api():
    # A dummy endpoint that simulates receiving a JSON payload from an LLM
    api_url = "https://jsonplaceholder.typicode.com/posts"
    
    # 2a. The Headers (Authentication Layer)
    # In a real scenario, "Bearer YOUR_API_KEY" goes here.
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-mock-api-key-12345"
    }
    
    # 2b. The Payload (Intelligence Layer)
    # This represents exactly what we send to OpenAI or Anthropic.
    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {"role": "system", "content": "You analyze user sentiment."},
            {"role": "user", "content": "Analyze the sentiment for user 'Alice'."}
        ]
    }
    
    print("--- TRANSMITTING HTTP POST REQUEST ---")
    try:
        # 3. SYNCHRONOUS EXECUTION
        # Transmitting the payload over the web and waiting for the response.
        response = requests.post(api_url, headers=headers, json=payload, timeout=5)
        
        # Raise an exception immediately if the server returns a 404, 401, or 500 error
        response.raise_for_status() 
        
        print(f"Network Success! Status Code: {response.status_code}\n")
        
        # Simulating the raw, messy JSON string that an LLM might return
        # (In reality, we would extract this from response.json()["choices"][0]["message"]["content"])
        mock_llm_output = {
            "user_name": "Alice",
            "sentiment_score": "88",       # Notice this is a STRING, but Pydantic expects an INT
            "is_flagged_for_review": "false" # Notice this is a STRING, but Pydantic expects a BOOL
        }
        
        return mock_llm_output
        
    except requests.exceptions.RequestException as e:
        print(f"[NETWORK CRASH] Failed to reach API: {e}")
        return None

# 4. END-TO-END EXECUTION & VALIDATION
if __name__ == "__main__":
    
    # Step A: Get the raw data from the web
    raw_api_data = analyze_user_data_via_api()
    
    if raw_api_data:
        print("--- VALIDATING RAW LLM OUTPUT ---")
        print(f"Raw Data received: {raw_api_data}\n")
        
        try:
            # Step B: Pass the raw dictionary into our strict Pydantic model
            # This is where the magic happens (Auto-casting strings to ints/bools)
            validated_insight = UserInsight(**raw_api_data)
            
            print("--- VALIDATION SUCCESSFUL! ---")
            print(f"Secured Object: {validated_insight}")
            
            # Now your IDE knows exactly what data types these are!
            print(f"Cleaned Score (Now a true Integer): {validated_insight.sentiment_score + 10}")
            
        except ValidationError as e:
            # Step C: Fail Fast if the LLM completely hallucinated the structure
            print(f"[VALIDATION CRASH] The LLM failed to match our schema:\n{e.json()}")
