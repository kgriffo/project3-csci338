from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/hello")
async def root():
    return {"message": "Hello World"}