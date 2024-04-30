from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/hello")
async def api():
    return {"message": "Hello World"}