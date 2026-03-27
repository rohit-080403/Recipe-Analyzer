from pydantic import BaseModel
from typing import List, Optional

# ── Request ──────────────────────────────────────────────
class IngredientRequest(BaseModel):
    ingredients: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "ingredients": ["chicken", "garlic", "olive oil", "lemon"]
            }
        }

# ── Nutrition ────────────────────────────────────────────
class NutritionInfo(BaseModel):
    calories: int
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float

# ── Single Recipe ─────────────────────────────────────────
class Recipe(BaseModel):
    name: str
    description: str
    cook_time_minutes: int
    difficulty: str                    # Easy / Medium / Hard
    match_percentage: int             # How many ingredients user has
    ingredients_needed: List[str]     # All ingredients for recipe
    missing_ingredients: List[str]    # Ingredients user doesn't have
    steps: List[str]                  # Cooking steps
    nutrition: NutritionInfo

# ── Response ──────────────────────────────────────────────
class RecipeResponse(BaseModel):
    recipes: List[Recipe]
    total_found: int
    ingredients_used: List[str]