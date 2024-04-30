from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/", StaticFiles(directory="ui/dist", html=True), name="ui")


@app.get("/api/v1/hello")
async def api():
    return {"message": "Hello World"}