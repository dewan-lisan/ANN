import os
import json
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Environment config
PROJECT_ID = os.environ.get("PROJECT_ID", "s86338-cc01fdd6")  # "graphical-elf-469607-p4")
LOCATION = os.environ.get("GCP_LOCATION", "europe-north1")

vertexai.init(project=PROJECT_ID, location=LOCATION)


def to_json(response_text):
    try:
        response_json = json.loads(response_text)
        return response_json
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        return None


def gen_diet_plan(params):
    response_schema = {
      "title": "Diet Plan Schema",
      "type": "object",
      "properties": {
        "diet_plan": {
          "type": "object",
          "properties": {
            "summary": {
              "type": "object",
              "properties": {
                "target_calories": { "type": "number" },
                "target_protein_g": { "type": "number" },
                "target_carbs_g": { "type": "number" },
                "target_fat_g": { "type": "number" },
                "notes": { "type": "string" }
              },
              "required": [
                "target_calories",
                "target_protein_g",
                "target_carbs_g",
                "target_fat_g",
                "notes"
              ]
            },
            "days": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "day": { "type": "integer", "minimum": 1 },
                  "daily_totals": {
                    "type": "object",
                    "properties": {
                      "calories": { "type": "number" },
                      "protein": { "type": "number" },
                      "carbs": { "type": "number" },
                      "fat": { "type": "number" },
                      "fiber": { "type": "number" },
                      "sugar": { "type": "number" },
                      "sodium": { "type": "number" }
                    },
                    "required": [
                      "calories",
                      "protein",
                      "carbs",
                      "fat",
                      "fiber",
                      "sugar",
                      "sodium"
                    ]
                  },
                  "meals": {
                    "type": "object",
                    "properties": {
                      "breakfast": { "$ref": "#/$defs/meal" },
                      "lunch": { "$ref": "#/$defs/meal" },
                      "dinner": { "$ref": "#/$defs/meal" },
                      "snack": { "$ref": "#/$defs/meal" }
                    },
                    "required": ["breakfast", "lunch", "dinner", "snack"]
                  }
                },
                "required": ["day", "daily_totals", "meals"]
              }
            }
          },
          "required": ["summary", "days"]
        }
      },
      "required": ["diet_plan"],
      "$defs": {
        "meal": {
          "type": "object",
          "properties": {
            "name": { "type": "string"},
            "description": { "type": "string"},
            "calories": { "type": "number" },
            "protein": { "type": "number" },
            "carbs": { "type": "number" },
            "fat": { "type": "number" },
            "fiber": { "type": "number" },
            "sugar": { "type": "number" },
            "sodium": { "type": "number" }
          },
          "required": [
            "name",
            "description",
            "calories",
            "protein",
            "carbs",
            "fat",
            "fiber",
            "sugar",
            "sodium"
          ]
        }
      }
    }

    generation_config = GenerationConfig(
        response_mime_type="application/json",
        response_schema=response_schema
    )

    try:
        model = GenerativeModel(model_name="gemini-2.5-pro", generation_config=generation_config)
        prompt = f"""
        Create a personalized 7-day diet plan for a person with this info:
        {params}

        Make the plan nutritionally balanced.
        Return the meal plan in strict JSON format using the schema {response_schema}. Each meal must include: name, calories, protein (g), carbs (g), fat (g), fiber (g), sugar (g), sodium (mg).
        """

        response = model.generate_content(prompt)
        print(response.text)
        return response.text
    except Exception as e:
        # st.error(f"AI error generating diet plan: {str(e)}")
        print("Error generating plan")
        print(str(e))
        return None
