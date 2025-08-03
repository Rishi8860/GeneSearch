# main.py
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
# from gemini import attribute_Prediction
from workflow import attribute_Prediction
from google.api_core.exceptions import ResourceExhausted

# Initialize the FastAPI app
app = FastAPI()

# --- CORS (Cross-Origin Resource Sharing) ---
# This allows the HTML frontend (running on a different port)
# to communicate with this backend.
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "null", # Important for local file testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
# Defines the expected structure of the incoming request data.
class SearchQuery(BaseModel):
    query: str

# --- API Endpoint ---
@app.post("/search")
def search_variants(search_query: SearchQuery):
    """
    Receives a search query and returns a mock list of gene variants.
    In a real application, this is where you would query your database
    or run your analysis based on the search_query.query.
    """
    try:
        query_text = search_query.query
        attributes = attribute_Prediction(query_text)
        results = []
        for i in attributes['classification']:
            results.append({
                "value": i['attribute'],
                "reason": i['reason']
            })

        return results
    except ResourceExhausted:
        raise HTTPException(status_code=429, detail="Gemini API quota exceeded. Please try again later.")

