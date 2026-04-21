from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

app = FastAPI(title="Smart Food & Health Context Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models for the stateless API request
class UserContextRequest(BaseModel):
    craving: str
    circadian_rhythm: str  # e.g., "morning", "afternoon", "late_night"
    cognitive_load: str    # e.g., "low", "medium", "high"
    metabolic_state: str   # e.g., "fasted", "recent_heavy_meal", "optimal"

# Mock Data Structure for Cravings and Alternatives
ALTERNATIVES_DB: Dict[str, List[Dict[str, Any]]] = {
    "fried chicken": [
        {"name": "Grilled Salmon & Asparagus", "lipid_heavy": False, "carb_heavy": False, "protein_rich": True, "omega_3": True},
        {"name": "Baked Chicken Breast & Quinoa", "lipid_heavy": False, "carb_heavy": True, "protein_rich": True, "omega_3": False},
        {"name": "Air-Fried Chickpea Tofu", "lipid_heavy": False, "carb_heavy": True, "protein_rich": True, "omega_3": False}
    ],
    "pizza": [
        {"name": "Cauliflower Crust Margherita", "lipid_heavy": False, "carb_heavy": False, "protein_rich": False, "omega_3": False},
        {"name": "Whole Wheat Chicken Flatbread", "lipid_heavy": False, "carb_heavy": True, "protein_rich": True, "omega_3": False},
        {"name": "Stuffed Bell Peppers with Turkey", "lipid_heavy": False, "carb_heavy": False, "protein_rich": True, "omega_3": False}
    ],
    "sugary donut": [
        {"name": "Greek Yogurt with Mixed Berries", "lipid_heavy": False, "carb_heavy": False, "protein_rich": True, "omega_3": False, "sugar_spike": True},
        {"name": "Dark Chocolate (85%) & Almonds", "lipid_heavy": True, "carb_heavy": False, "protein_rich": False, "omega_3": False, "sugar_spike": False},
        {"name": "Oatmeal with Cinnamon & Apple", "lipid_heavy": False, "carb_heavy": True, "protein_rich": False, "omega_3": False, "sugar_spike": False}
    ],
    "donut": [
        {"name": "Greek Yogurt with Mixed Berries", "lipid_heavy": False, "carb_heavy": False, "protein_rich": True, "omega_3": False, "sugar_spike": True},
        {"name": "Dark Chocolate (85%) & Almonds", "lipid_heavy": True, "carb_heavy": False, "protein_rich": False, "omega_3": False, "sugar_spike": False},
        {"name": "Oatmeal with Cinnamon & Apple", "lipid_heavy": False, "carb_heavy": True, "protein_rich": False, "omega_3": False, "sugar_spike": False}
    ],
    "burger": [
        {"name": "Lean Turkey Burger on Lettuce Wrap", "lipid_heavy": False, "carb_heavy": False, "protein_rich": True, "omega_3": False},
        {"name": "Portobello Mushroom Burger", "lipid_heavy": False, "carb_heavy": True, "protein_rich": False, "omega_3": False},
        {"name": "Bison Burger with Sweet Potato Wedges", "lipid_heavy": False, "carb_heavy": True, "protein_rich": True, "omega_3": False}
    ]
}

class ContextEngine:
    """Heuristic scoring algorithm for food optimization."""
    
    @staticmethod
    def evaluate(craving_category: str, context: UserContextRequest) -> Dict[str, Any]:
        alternatives: Optional[List[Dict[str, Any]]] = ALTERNATIVES_DB.get(craving_category.lower())
        if not alternatives:
            raise ValueError(f"Craving '{craving_category}' not found in database.")

        best_score: int = -9999
        best_alternative: Optional[Dict[str, Any]] = None
        rationale: str = ""

        for alt in alternatives:
            score: int = 100  # Base score
            reasons: List[str] = []

            # 1. Circadian Rhythm Heuristics
            if context.circadian_rhythm == "late_night":
                if alt.get("carb_heavy"):
                    score -= 40
                    reasons.append("Heavy carbohydrates late at night disrupt slow-wave sleep.")
                if alt.get("sugar_spike"):
                    score -= 50
                    reasons.append("Sugary foods before bed spike insulin, interfering with melatonin production.")
            elif context.circadian_rhythm == "morning":
                if alt.get("carb_heavy"):
                    score += 10 # Carbs okay for morning energy
                
            # 2. Cognitive Load Heuristics
            if context.cognitive_load == "high":
                if alt.get("omega_3"):
                    score += 30
                    reasons.append("Omega-3 fatty acids reduce neuro-inflammation and support high cognitive demand.")
                if alt.get("lipid_heavy") and not alt.get("omega_3"):
                    score -= 20
                    reasons.append("Heavy saturated fats can induce sluggishness and cognitive fog.")
            
            # 3. Metabolic State Heuristics
            if context.metabolic_state == "recent_heavy_meal":
                if alt.get("carb_heavy") or alt.get("lipid_heavy"):
                    score -= 50
                    reasons.append("Adding dense macronutrients shortly after a heavy meal overwhelms metabolic processing.")
            elif context.metabolic_state == "fasted":
                if alt.get("protein_rich"):
                    score += 20
                    reasons.append("High protein is ideal for breaking a fast to preserve lean body mass.")

            if score > best_score:
                best_score = score
                best_alternative = alt
                if reasons:
                    rationale = " ".join(list(set(reasons)))
                else:
                    rationale = "This is a balanced alternative that suits your current physiological state."

        # Calculate is_healthy boolean
        is_healthy: bool = best_score > 80

        return {
            "original_craving": context.craving,
            "recommended_alternative": best_alternative["name"] if best_alternative else "Unknown",
            "score": best_score,
            "is_healthy": is_healthy,
            "scientific_rationale": rationale
        }

@app.post("/optimize-meal")
async def optimize_meal(request: UserContextRequest) -> Dict[str, Any]:
    try:
        craving_key: str = request.craving.lower()
        
        matched_key: Optional[str] = None
        for key in ALTERNATIVES_DB.keys():
            if key in craving_key or craving_key in key:
                matched_key = key
                break
                
        if not matched_key:
            raise HTTPException(status_code=404, detail="I'm not aware of this craving yet, but I'll look into it and update my database!")
            
        result: Dict[str, Any] = ContextEngine.evaluate(matched_key, request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
