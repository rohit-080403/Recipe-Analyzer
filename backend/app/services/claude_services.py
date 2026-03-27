import os
import json
import anthropic
from typing import List
from app.models.schemas import Recipe, NutritionInfo

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def build_prompt(ingredients: List[str]) -> str:
    ingredients_str = ", ".join(ingredients)
    return f"""
You are a professional chef and nutritionist.
A user has these ingredients: {ingredients_str}

Return ONLY a valid JSON array (no markdown, no explanation) of exactly 4 recipes they can make.
Each recipe must follow this exact structure:

[
  {{
    "name": "Recipe Name",
    "description": "Short 1-sentence description",
    "cook_time_minutes": 30,
    "difficulty": "Easy",
    "match_percentage": 85,
    "ingredients_needed": ["ingredient1", "ingredient2"],
    "missing_ingredients": ["ingredient3"],
    "steps": ["Step 1...", "Step 2...", "Step 3..."],
    "nutrition": {{
      "calories": 450,
      "protein_g": 32.5,
      "carbs_g": 45.0,
      "fat_g": 12.0,
      "fiber_g": 4.5
    }}
  }}
]

Rules:
- match_percentage = percentage of recipe ingredients the user already has
- missing_ingredients = ingredients NOT in the user's list
- nutrition is per serving
- difficulty is one of: Easy, Medium, Hard
- Return ONLY the JSON array, nothing else
"""

def get_recipes_from_claude(ingredients: List[str]) -> List[Recipe]:
    prompt = build_prompt(ingredients)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_text = message.content[0].text.strip()

    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    recipes_data = json.loads(raw_text)

    recipes = []
    for r in recipes_data:
        nutrition = NutritionInfo(**r["nutrition"])
        recipe = Recipe(
            name=r["name"],
            description=r["description"],
            cook_time_minutes=r["cook_time_minutes"],
            difficulty=r["difficulty"],
            match_percentage=r["match_percentage"],
            ingredients_needed=r["ingredients_needed"],
            missing_ingredients=r["missing_ingredients"],
            steps=r["steps"],
            nutrition=nutrition
        )
        recipes.append(recipe)

    return recipes