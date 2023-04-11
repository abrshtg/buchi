from fastapi import FastAPI
import uvicorn
from app.routers import adoptions, customers, pets, reports, users

description = """
Buchi Pet finder API helps you to find a pet. 🚀

## pets
You can:
* **Read pets**.
* **Post pets** (_Note: you have to be regesterd to make a post request_).
* **Update pets** (_not implemented_).
* **Delete pets** (_not implemented_).

## adoptions

* **Read adoptions**.
* **Post adoptions** (_Note: you have to be registerd an authenticated to make a post request_).
* **Update adoptions** (_not implemented_).
* **Delete adoptions** (_not implemented_).

## Users

You will be able to:

* **Register user**.
* **Login user** (_you will get a token when you logged in_).
* **Read current user**.

## Report 

* **Read report** (_you can get weekely adoption rate_)
"""

app = FastAPI(
    title="Buchi Pet finder API",
    description=description,
    version="1",
    contact={
        "name": "Abrham Mesfin",
        "email": "abrshtgam@gmail.com",
    }
)

app.include_router(adoptions.router, tags=['Adoptions'])
app.include_router(customers.router, tags=['Customers'])
app.include_router(pets.router, tags=['Pets'])
app.include_router(reports.router, tags=['Reports'])
app.include_router(users.router, tags=['users'])


@app.get('/', tags=['home'])
async def home():
    return {
        "docs": "https://buchi-api.onrender.com/docs",
        "redoc": "https://buchi-api.onrender.com/redoc"
    }
