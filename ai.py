from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def parse_ngo_query(query):
    prompt = f"""
    User query: "{query}"
    Extract key criteria for matching food offers as a JSON dict.
    Possible keys: food_type (string), quantity (int), location (string), max_expiration (ISO datetime string like '2026-01-11T20:00:00').
    If not mentioned, omit the key. Be precise.
    Example input: "Vegetarian rice for 15 kids in Abuja before 8 PM tonight"
    Example output: {{"food_type": "vegetarian rice", "quantity": 15, "location": "Abuja", "max_expiration": "2026-01-11T20:00:00"}}
    """
    response = client.models.generate_content(
        model= 'gemini-2.5-flash',
        contents = prompt
    )
    # Parse the JSON from response (handle manually or use json.loads)
    import json
    try:
        criteria = json.loads(response.text.strip())
    except:
        criteria = {}  # Fallback
    print(response.text)
    return criteria

def generate_match_summary(matches):
    if not matches:
        return "No matches found—try a broader search!"
    summaries = []
    for match in matches:
        summaries.append(f"Food: {match[1]}, Qty: {match[2]}, Expires: {match[3]}, Location: {match[4]}, Contact: {match[5]}")
    prompt = f"Generate a polite, concise list of matches:\n" + "\n".join(summaries)
    response = client.models.generate_content(model = 'gemini-2.5-flash', contents = prompt)
    return response.text