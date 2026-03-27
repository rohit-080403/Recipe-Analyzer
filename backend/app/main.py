from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import recipe
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Recipe Ingredient Analyzer",
    description="Input ingredients, get recipes + nutrition via Claude AI",
    version="1.0.0"
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(recipe.router, prefix="/api", tags=["Recipes"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Recipe Analyzer API is running"}