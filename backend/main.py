from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import your route files (we'll create these next)
from routes import overview, cards, relics, encounters

app = FastAPI()

# allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later change to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register routes
app.include_router(overview.router, prefix="/api")
app.include_router(cards.router, prefix="/api")
app.include_router(relics.router, prefix="/api")
app.include_router(encounters.router, prefix="/api")

# simple test route
@app.get("/")
def root():
    return {"message": "SpireStats backend running"}