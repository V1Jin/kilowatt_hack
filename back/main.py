from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from external_data import final_get

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/external-data")
async def solve_assignment(data: dict = Body(...)):
    try:
        text = data.get("text")   
        result = final_get(text)
        return {"status": "success", "result": result}
        
    except Exception as e:
        print("Ошибка на сервере:", str(e)) 
        raise HTTPException(status_code=500, detail=str(e))
# uvicorn main:app --reload --host 0.0.0.0 --port 8000