import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-70b-8192"

def get_mongo_query_from_groq(nl_query: str):
    print(f"🧠 Received NL Query: {nl_query}")
    prompt = (
        f"Convert the following natural language query into a MongoDB query. "
        f"Return a JSON object with keys like 'collection', 'find', 'project', 'aggregate', 'sort', and 'chart' where needed.\n"
        f"Query: {nl_query}"
    )

    if not GROQ_API_KEY:
        print("⚠️ No GROQ API key found, using fallback.")
        return get_mock_fallback(nl_query)

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that translates natural language into MongoDB queries."
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            }
        )
        response.raise_for_status()
        raw_text = response.json()["choices"][0]["message"]["content"]

        print(f"🤖 Raw response from Groq:\n{raw_text}")

        json_text = raw_text[raw_text.find("{"):raw_text.rfind("}") + 1]
        parsed = json.loads(json_text)

        print(f"✅ Parsed MongoDB query: {parsed}")
        return parsed

    except Exception as e:
        print(f"❌ Groq failed, using fallback. Error: {e}")
        return get_mock_fallback(nl_query)


def get_mock_fallback(nl_query: str):
    print("🧪 Using fallback for:", nl_query)

    nl_query = nl_query.lower()

    if "temperature" in nl_query:
        return {
            "collection": "parameter_metadata",
            "aggregate": [
                {"$project": {"_id": 0, "timestamp": 1, "temperature": 1}},
                {"$sort": {"timestamp": 1}}
            ],
            "chart": {
                "title": "Temperature Over Time",
                "xlabel": "timestamp",
                "ylabel": "temperature"
            }
        }

    if "current" in nl_query:
        return {
            "collection": "parameter_metadata",
            "aggregate": [
                {"$project": {"_id": 0, "timestamp": 1, "current": 1}},
                {"$sort": {"timestamp": 1}}
            ],
            "chart": {
                "title": "Current Over Time",
                "xlabel": "timestamp",
                "ylabel": "current"
            }
        }

    if "voltage" in nl_query:
        return {
            "collection": "parameter_metadata",
            "aggregate": [
                {"$project": {"_id": 0, "timestamp": 1, "voltage": 1}},
                {"$sort": {"timestamp": 1}}
            ],
            "chart": {
                "title": "Voltage Over Time",
                "xlabel": "timestamp",
                "ylabel": "voltage"
            }
        }

    if "co2" in nl_query:
        return {
            "collection": "parameter_metadata",
            "aggregate": [
                {"$match": {"co2_level": {"$gt": 800}}},
                {"$sort": {"timestamp": 1}}
            ],
            "chart": {
                "title": "High CO2 Levels",
                "xlabel": "timestamp",
                "ylabel": "co2_level"
            }
        }

    # Default fallback
    return {
        "collection": "parameter_metadata",
        "find": {}
    }
