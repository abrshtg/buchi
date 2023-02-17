from fastapi import FastAPI
from fastapi.responses import FileResponse
from routers import adoptions, customers, pets, reports
app = FastAPI()

app.include_router(adoptions.router)
app.include_router(customers.router)
app.include_router(pets.router)
app.include_router(reports.router)


@app.get('/images/{img}')
def image(img: str):
    return FileResponse("images/" + img)
