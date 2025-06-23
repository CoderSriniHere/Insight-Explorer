import json
from fastapi import HTTPException
from pymongo import MongoClient
from bson import json_util
from chart_generator import generate_chart
from groq_helper import get_mongo_query_from_groq

client = MongoClient("mongodb://localhost:27017/")
db = client["ai_intern"]

def run_query_from_nl(nl_query: str):
    print(f"\n🧠 Received NL Query: {nl_query}")

    parsed = get_mongo_query_from_groq(nl_query)
    if not isinstance(parsed, dict):
        raise HTTPException(status_code=500, detail="Invalid response format from Groq.")

    # Handle legacy nested structure
    if "mongo_query" in parsed:
        parsed = {**parsed["mongo_query"], "chart": parsed.get("chart")}

    print("🧠 Parsed MongoDB Query from Groq:")
    print(json.dumps(parsed, indent=2))

    # Use fallback collection if not defined
    collection_name = parsed.get("collection")
    if collection_name in [None, "", "your_collection_name"]:
        collection_name = "parameter_metadata"
        parsed["collection"] = collection_name

    collection = db[collection_name]
    data = []

    try:
        if "aggregate" in parsed or "pipeline" in parsed:
            pipeline = parsed.get("aggregate") or parsed.get("pipeline")
            if isinstance(pipeline, dict):
                raise HTTPException(status_code=500, detail="Pipeline must be a list, not a dict.")
            print(f"📊 Running aggregation on collection `{collection_name}` with pipeline:")
            for stage in pipeline:
                print(stage)
            data = list(collection.aggregate(pipeline))
        elif "find" in parsed:
            query = parsed["find"]
            projection = parsed.get("project", {})
            print(f"🔍 Running `find` on collection `{collection_name}` with filter:")
            print(json.dumps(query, indent=2))
            cursor = collection.find(query, projection)
            if "sort" in parsed:
                print(f"🔃 Sorting with: {parsed['sort']}")
                cursor = cursor.sort(list(parsed["sort"].items()))
            data = list(cursor)
        else:
            raise HTTPException(status_code=500, detail="Unsupported MongoDB query format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB query execution failed: {e}")

    print("✅ Raw MongoDB Data:")
    print(data if data else "No matching records found.")

    # Chart support
    if "chart" in parsed:
        return generate_chart(data, parsed["chart"])

    # Natural language fallback
    if not data:
        return {"response": "No results found for the given query."}
    else:
        return {
            "response": f"Found {len(data)} matching documents.",
            "documents": json.loads(json_util.dumps(data))
        }
