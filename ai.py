from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def parse_ngo_query(query):
    prompt = f"""
You are a precise criteria extractor for food donation matching.
Given this user request: "{query}"

Extract ONLY the mentioned criteria as valid JSON.
Use these exact keys (only include if clearly mentioned):
- "food_type": string (main food description, be specific)
- "quantity": integer (minimum portions needed)
- "location": string (city/area)
- "max_expiration": ISO datetime string (latest acceptable expiration, format: YYYY-MM-DDTHH:MM:SS)

Rules:
- If a key is not mentioned → DO NOT include it
- Never guess or add information
- Output ONLY valid JSON object, nothing else (no explanations, no markdown)

Examples:
User: "Need rice for 20 people in Abuja tonight"
Output: {{"food_type": "rice", "quantity": 20, "location": "Abuja"}}

User: "Any food for 10 kids"
Output: {{"quantity": 10}}
"""
    response = client.models.generate_content(model = 'gemini-2.5-flash', contents = prompt)
    text = response.text.strip()
    
    # Clean common LLM markdown junk
    if text.startswith("```json"):
        text = text.split("```json")[1].split("```")[0].strip()
    elif text.startswith("```"):
        text = text.split("```")[1].strip()
    
    import json
    try:
        criteria = json.loads(text)
        return criteria
    except Exception:
        #st.error("AI couldn't understand the query well. Try being more specific!")
        return {}  # empty → broad search as fallback

def generate_match_summary(matches):
    if not matches:
        return "No matches found—try a broader search!"
    summaries = []
    for match in matches:
        summaries.append(f"Food: {match[1]}, Qty: {match[2]}, Expires: {match[3]}, Location: {match[4]}, Contact: {match[5]}")
    prompt = f"Generate a polite, concise list of matches:\n" + "\n".join(summaries)
    response = client.models.generate_content(model = 'gemini-2.5-flash', contents = prompt)
    return response.text