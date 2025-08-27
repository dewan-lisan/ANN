import json

import streamlit as st
from planner_vertexai import gen_diet_plan


def generate_diet_plan(params: dict):
    with st.spinner("🧠 Generating your personalized diet plan..."):
        diet_plan = gen_diet_plan(json.dumps(params, indent=2))
        if diet_plan:
            st.session_state.diet_plan = diet_plan
            st.success("✅ Diet plan generated successfully!")
        else:
            st.error("❌ Failed to generate diet plan. Please try again.")
    # st.json(params)  # For now just show collected inputs

    if st.session_state.diet_plan:
        display_diet_plan()


def display_diet_plan():
    if st.session_state.diet_plan:
        st.subheader("Your Personalized Diet Plan")
        st.markdown("---")
        st.markdown(st.session_state.diet_plan)
    else:
        st.info("No diet plan generated yet.")

        # Download button
    st.download_button(
        label="Download Plan",
        data=st.session_state.diet_plan,
        file_name="my_diet_plan.md",
        mime="text/markdown"
    )

def next_step():
    st.session_state.step += 1


def prev_step():
    st.session_state.step -= 1


def main():
    # Initialize session state for user inputs

    if "diet_plan" not in st.session_state:
        st.session_state.diet_plan = None
    # Custom CSS styling

    # Initialize wizard step tracker
    if "step" not in st.session_state:
        st.session_state.step = 1

    # Initialize dictionary to capture inputs
    if "inputs" not in st.session_state:
        st.session_state.inputs = {}

    st.title("🥗 Diet Planner Wizard")
    st.set_page_config(page_title="Diet Planner Wizard", page_icon="🥗", layout="centered")

    # ---- Step 1: Demographics + Goals (Mandatory) ----
    if st.session_state.step == 1:
        st.subheader("Basic Demographics & Goals")

        st.session_state.inputs["age"] = st.number_input("Age", min_value=5, max_value=100, step=1,
                                                         value=st.session_state.inputs.get("age", 25))
        st.session_state.inputs["gender"] = st.selectbox("Gender", ["Male", "Female", "Other"],
                                                         index=["Male", "Female", "Other"].index(
                                                             st.session_state.inputs.get("gender", "Male")))
        st.session_state.inputs["height"] = st.number_input("Height (cm)", min_value=50, max_value=250,
                                                            value=st.session_state.inputs.get("height", 170))
        st.session_state.inputs["weight"] = st.number_input("Weight (kg)", min_value=10, max_value=300,
                                                            value=st.session_state.inputs.get("weight", 70))
        st.session_state.inputs["activity"] = st.selectbox(
            "Activity Level",
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Athlete"],
            index=0 if "activity" not in st.session_state.inputs else
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Athlete"].index(
                st.session_state.inputs["activity"])
        )

        st.session_state.inputs["goal"] = st.radio("What is your main goal?",
                                                   ["Lose Weight", "Gain Muscle", "Maintain Weight", "Medical Diet",
                                                    "General Wellness"],
                                                   index=0 if "goal" not in st.session_state.inputs else
                                                   ["Lose Weight", "Gain Muscle", "Maintain Weight", "Medical Diet",
                                                    "General Wellness"].index(
                                                       st.session_state.inputs["goal"])
                                                   )
        st.session_state.inputs["target_weight"] = st.number_input("Target Weight (kg)", min_value=10,
                                                                   max_value=300,
                                                                   value=st.session_state.inputs.get(
                                                                       "target_weight", 65))
        st.session_state.inputs["timeline"] = st.text_input("Target Timeline (e.g., 2 months, 6 weeks)",
                                                            st.session_state.inputs.get("timeline", ""))

        st.button("Next ➡️", on_click=next_step)

        # Generate button outside the form
        if st.button("Generate Diet Plan ✅", key="gen_plan_step1"):
            generate_diet_plan(st.session_state.inputs)

    # ---- Step 2: Health Conditions + Lifestyle (Optional) ----
    elif st.session_state.step == 2:
        st.subheader("Health Conditions & Lifestyle")

        st.session_state.inputs["allergies"] = st.multiselect("Any food allergies?",
                                                              ["Nuts", "Gluten", "Shellfish", "Lactose", "Soy",
                                                               "Eggs"],
                                                              default=st.session_state.inputs.get("allergies", []))
        st.session_state.inputs["conditions"] = st.multiselect("Any health conditions?",
                                                               ["Diabetes", "Hypertension", "Kidney Disease",
                                                                "Other"],
                                                               default=st.session_state.inputs.get("conditions",
                                                                                                   []))
        st.session_state.inputs["diet_type"] = st.multiselect("Diet Type",
                                                              ["Vegetarian", "Vegan", "Pescatarian", "Halal",
                                                               "Kosher"],
                                                              default=st.session_state.inputs.get("diet_type", []))

        col1, col2 = st.columns(2)
        with col1:
            st.button("⬅️ Back", on_click=prev_step)
        with col2:
            st.button("Next ➡️", on_click=next_step)

        # Generate button outside the form
        if st.button("Generate Diet Plan ✅", key="gen_plan_step2"):
            generate_diet_plan(st.session_state.inputs)

    # ---- Step 3: Cuisine + Meal Structure (Optional) ----
    elif st.session_state.step == 3:
        st.subheader("Cuisine & Food Style")

        st.session_state.inputs["cuisines"] = st.multiselect("Preferred Cuisines",
                                                             ["Bangladeshi", "Indian", "Italian", "Chinese",
                                                              "Japanese", "Mediterranean", "Middle Eastern",
                                                              "Other"],
                                                             default=st.session_state.inputs.get("cuisines", []))
        st.session_state.inputs["dish_pref"] = st.radio("Meal Style",
                                                        ["Traditional", "Fusion", "Global"],
                                                        index=0 if "dish_pref" not in st.session_state.inputs else
                                                        ["Traditional", "Fusion", "Global"].index(
                                                            st.session_state.inputs["dish_pref"]))
        st.session_state.inputs["meal_pattern"] = st.radio("Preferred Meal Structure",
                                                           ["3 Meals a Day", "5-6 Small Meals",
                                                            "One Main + Light Meals", "Intermittent Fasting"],
                                                           index=0 if "meal_pattern" not in st.session_state.inputs else
                                                           ["3 Meals a Day", "5-6 Small Meals",
                                                            "One Main + Light Meals", "Intermittent Fasting"].index(
                                                               st.session_state.inputs["meal_pattern"]))

        st.button("⬅️ Back", on_click=prev_step)

        # Generate button outside the form
        if st.button("Generate Diet Plan ✅", key="gen_plan_step3"):
            generate_diet_plan(st.session_state.inputs)


if __name__ == "__main__":
    main()
