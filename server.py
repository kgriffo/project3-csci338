from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select

from models import AutoModels

engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@db:5432/dvdrental", echo=True
)


auto_models = None


async def lifespan(app):
    print("startup")
    global auto_models
    auto_models = await AutoModels.create(engine)
    yield
    print("shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/api/v1/hello")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/films")
async def films():
    Film = await auto_models.get("film")

    results = []

    async with AsyncSession(engine) as session:
        films = await session.execute(select(Film))
        for film in films.scalars().all():
            results.append(
                {
                    "title": film.title,
                    "description": film.description,
                    "id": film.film_id,
                }
            )
    return results

@app.get("/film/{id}", response_class=HTMLResponse)
async def film(id: int):
    with open("ui/dist/film.html") as file:
        return file.read()
    
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("ui/dist/film.html") as file:
        return file.read()


# ChatGPT helped out with this
@app.get("/api/v1/film/{id}")
async def get_film(id: int):
    async with AsyncSession(engine) as session:
        Film = await auto_models.get("film")
        result = await session.execute(select(Film).where(Film.film_id == id))
        film = result.scalars().first()

        if film:
            return {
                "title": film.title,
                "description": film.description,
                "id": film.film_id,
            }
        else:
            return {"error": "Film not found"}
        
@app.delete("/api/v1/film/{id}")
async def api_v1_film_delete(id: int):
    Film = await auto_models.get("film")

    async with AsyncSession(engine) as session:
        film = await session.execute(select(Film).where(Film.film_id == id))
        film = film.scalars().first()
        if film:
            await session.delete(film)
            await session.commit()
            return {"ok": True}
        else:
            return {"ok": False, "reason": "not found"}


app.mount("/", StaticFiles(directory="ui/dist", html=True), name="ui")