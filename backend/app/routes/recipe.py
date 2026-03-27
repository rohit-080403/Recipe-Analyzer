from fastapi import APIRouter, HTTPException
from app.models.schemas import IngredientRequest, RecipeResponse
from app.services.claude_services import get_recipes_from_claude
from app.utils.parser import parse_ingredients

router = APIRouter()

@router.post("/analyze", response_model=RecipeResponse)
async def analyze_ingredients(request: IngredientRequest):
    if not request.ingredients:
        raise HTTPException(status_code=400, detail="Ingredients list cannot be empty")

    # Clean and normalize
    cleaned = parse_ingredients(request.ingredients)

    if not cleaned:
        raise HTTPException(status_code=400, detail="No valid ingredients found after parsing")

    try:
        recipes = get_recipes_from_claude(cleaned)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

    return RecipeResponse(
        recipes=recipes,
        total_found=len(recipes),
        ingredients_used=cleaned
    )