from fastapi import FastAPI
from app.routers import adoptions, customers, pets, reports
app = FastAPI()

app.include_router(adoptions.router)
app.include_router(customers.router)
app.include_router(pets.router)
app.include_router(reports.router)


@app.get('/')
def home():
    return {"buchi_api_swagger_docs": "https://buchi-api.onrender.com/docs"}
