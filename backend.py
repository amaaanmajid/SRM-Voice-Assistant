# backend.py

from fastapi import FastAPI
from pydantic import BaseModel
from personal import get_srm_response  # Import from your SRM chatbot module

app = FastAPI()

# Model for receiving input
class QueryRequest(BaseModel):
    input: str

# Endpoint to process the query and return the response
@app.post("/api/assistant")
async def assistant(query: QueryRequest):
    response = get_srm_response(query.input)
    return {"response": response}

# If you want CORS, add the middleware (optional)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict this based on your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
