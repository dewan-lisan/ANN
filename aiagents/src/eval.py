import pandas as pd

# Nutritional guidelines for validation based on WHO/USDA values
GUIDELINES = {
    "calories": (2000, 2500),       # kcal/day
    "protein_pct": (0.10, 0.35),    # fraction of calories
    "carbs_pct": (0.45, 0.65),
    "fat_pct": (0.20, 0.35),
    "fiber": (25, 35),              # g/day
    "sugar_pct": (0, 0.10),         # of total kcal
    "sodium": (0, 2300),            # mg/day
}


def evaluate_diet(df: pd.DataFrame):
    """Evaluate each day against guidelines, return compliance DataFrame."""
    results = []
    for _, row in df.iterrows():
        kcal = row["calories"]
        protein_pct = (row["protein"] * 4) / kcal
        carbs_pct = (row["carbs"] * 4) / kcal
        fat_pct = (row["fat"] * 9) / kcal
        sugar_pct = (row["sugar"] * 4) / kcal

        results.append({
            "day": row["day"],
            "calories_ok": GUIDELINES["calories"][0] <= kcal <= GUIDELINES["calories"][1],
            "protein_ok": GUIDELINES["protein_pct"][0] <= protein_pct <= GUIDELINES["protein_pct"][1],
            "carbs_ok": GUIDELINES["carbs_pct"][0] <= carbs_pct <= GUIDELINES["carbs_pct"][1],
            "fat_ok": GUIDELINES["fat_pct"][0] <= fat_pct <= GUIDELINES["fat_pct"][1],
            "fiber_ok": GUIDELINES["fiber"][0] <= row["fiber"] <= GUIDELINES["fiber"][1],
            "sugar_ok": sugar_pct <= GUIDELINES["sugar_pct"][1],
            "sodium_ok": row["sodium"] <= GUIDELINES["sodium"][1],
        })
    return pd.DataFrame(results)