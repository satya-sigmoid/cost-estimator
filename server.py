from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import List
from llm.llm import run_llm_pipeline

app = FastAPI()

class MarketInput(BaseModel):
    market: str
    multiplier: float
    start_month: int
    
class GenerateRequest(BaseModel):
    image_uri: str
    client_name: str
    use_case_name: str
    markets: List[MarketInput]
    
@app.post("/generate")
def generate_cost(req: GenerateRequest):
    result = run_llm_pipeline(req.image_uri,  req.client_name, req.use_case_name, 
            [m.model_dump() for m in req.markets])
    return {
        "status": "success",
        **result
    }
