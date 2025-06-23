from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from query_handler import run_query_from_nl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
async def process_query(request: Request):
    try:
        body = await request.json()
        nl_query = body.get("query")
        if not nl_query:
            return {"error": "No query provided."}
        return run_query_from_nl(nl_query)
    except Exception as e:
        return {"error": str(e)}
