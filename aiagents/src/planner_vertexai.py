from vertexai.preview.generative_models import GenerativeModel
import streamlit as st
import vertexai
import os

# Environment config
PROJECT_ID = os.environ.get("PROJECT_ID", "s86338-cc01fdd6")  # "graphical-elf-469607-p4")
LOCATION = os.environ.get("GCP_LOCATION", "europe-north1")

vertexai.init(project=PROJECT_ID, location=LOCATION)


def gen_diet_plan(params):
    try:
        model = GenerativeModel("gemini-2.5-pro")
        prompt = f"""
        Create a personalized 7-day diet plan for a person with this info:
        {params}

        Include:
        1. Daily calorie target
        2. Nutrient breakdown (protein, carbs, fat)
        3. Meal timing and frequency
        4. Food recommendations
        5. Hydration guidance

        Make the plan:
        - Nutritionally balanced
        - Practical for daily use
        - Culturally adaptable
        - With portion size guidance
        """

        response = model.generate_content(prompt)
        print(prompt)
        return response.text
    except Exception as e:
        # st.error(f"AI error generating diet plan: {str(e)}")
        print(str(e))
        return None
