import json
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from planner_vertexai import gen_diet_plan
from eval import evaluate_diet


def display_compliance_matrix(compliance_df):
    comp = compliance_df.melt(id_vars="day", var_name="Nutrient", value_name="Compliance")
    chart = alt.Chart(comp).mark_rect().encode(
        x=alt.X("Nutrient:N", title="Nutrient"),
        y=alt.Y("day:N", title="Day"),
        color=alt.Color(
            "Compliance:N",
            scale=alt.Scale(domain=[True, False], range=["#2ecc71", "#e74c3c"]),
            legend=alt.Legend(title="Compliance")
        ),
        tooltip=["day", "Nutrient", "Compliance"]
    ).properties(
        width=600,
        height=400,
        title="Diet Plan Compliance Matrix"
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16,
        anchor="middle"
    )
    st.altair_chart(chart, use_container_width=True)


# todo: improve radar chart select day bug fix
def display_radar_chart(day_row):
    labels = ["Protein %", "Carbs %", "Fat %", "Fiber", "Sugar %", "Sodium"]
    kcal = day_row["calories"]
    values = [
        (day_row["protein"] * 4) / kcal,
        (day_row["carbs"] * 4) / kcal,
        (day_row["fat"] * 9) / kcal,
        day_row["fiber"] / 30,
        (day_row["sugar"] * 4) / kcal,
        day_row["sodium"] / 2300,
    ]
    df_radar = pd.DataFrame({"Nutrient": labels, "Value": values})
    fig = px.line_polar(df_radar, r="Value", theta="Nutrient", line_close=True)
    fig.update_traces(fill="toself")
    st.plotly_chart(fig, use_container_width=True)


def parse_diet_plan(json_str):
    plan = json.loads(json_str)
    days = plan["diet_plan"]["days"]
    daily_data = [{"day": day["day"], **day["daily_totals"]} for day in days]
    return plan, pd.DataFrame(daily_data)


def generate_diet_plan(params: dict):
    with st.spinner("🧠 Generating your personalized diet plan..."):
        diet_plan = gen_diet_plan(json.dumps(params, indent=2))
        if diet_plan:
            st.session_state.diet_plan = diet_plan
            st.success("✅ Diet plan generated successfully!")
        else:
            st.error("❌ Failed to generate diet plan. Please try again.")

    if st.session_state.diet_plan:
        display_diet_plan()
        df = parse_diet_plan(st.session_state.diet_plan)[1]
        display_compliance(df)


def display_diet_plan():
    if st.session_state.diet_plan:
        st.subheader("Your Personalized Diet Plan")
        st.json(st.session_state.diet_plan, expanded=False)
    else:
        st.info("No diet plan generated yet.")
    st.download_button(
        label="Download Plan",
        data=st.session_state.diet_plan,
        file_name="my_diet_plan.md",
        mime="text/markdown"
    )


def display_compliance(df):
    compliance = evaluate_diet(df)
    st.subheader("📊 Daily Nutrient Totals")
    st.dataframe(df.set_index("day"))
    st.subheader("✅ Compliance Validation")
    st.dataframe(compliance.set_index("day"))
    display_compliance_matrix(compliance)
    # Store the selected day in session state
    if "selected_day" not in st.session_state:
        st.session_state.selected_day = df["day"].iloc[0]  # Default to the first day

    st.session_state.selected_day = st.selectbox(
        "Select day", df["day"].tolist(), index=df["day"].tolist().index(st.session_state.selected_day)
    )
    display_radar_chart(df[df["day"] == st.session_state.selected_day].iloc[0])


def store_diet_plan(plan):
    st.session_state.diet_plan = plan


def next_step():
    st.session_state.step += 1


def prev_step():
    st.session_state.step -= 1


def main():
    # Initialize session states
    if "diet_plan" not in st.session_state:
        st.session_state.diet_plan = None
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "inputs" not in st.session_state:
        st.session_state.inputs = {}

    st.title("🥗 Diet Planner Wizard")
    st.set_page_config(page_title="Diet Planner Wizard", page_icon="🥗", layout="centered")

    if st.session_state.step == 1:
        st.subheader("Basic Demographics & Goals")

        col1, col2 = st.columns(2)
        with col1:
            st.session_state.inputs.update({
                "age": st.number_input("Age", min_value=5, max_value=100, value=25),
                "height": st.number_input("Height (cm)", min_value=50, max_value=250, value=170),
                "activity": st.selectbox("Activity Level",
                                         ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Athlete"])
            })
        with col2:
            st.session_state.inputs.update({
                "gender": st.selectbox("Gender", ["Male", "Female", "Other"]),
                "weight": st.number_input("Weight (kg)", min_value=10, max_value=300, value=70),
                "target_weight": st.number_input("Target Weight (kg)", min_value=10, max_value=300, value=65)
            })
        st.session_state.inputs.update({
            "goal": st.radio("Main Goal",
                             ["Lose Weight", "Gain Muscle", "Maintain Weight", "Medical Diet", "General Wellness"]),
            "timeline": st.text_input("Target Timeline (e.g., 2 months)")
        })

        st.button("Next ➡️", on_click=next_step)
        if st.button("Generate Diet Plan ✅", key="gen_plan_step1"):
            generate_diet_plan(st.session_state.inputs)

    elif st.session_state.step == 2:
        st.subheader("Health Conditions & Lifestyle")

        st.session_state.inputs.update({
            "allergies": st.multiselect("Food Allergies", ["Nuts", "Gluten", "Shellfish", "Lactose", "Soy", "Eggs"]),
            "conditions": st.multiselect("Health Conditions", ["Diabetes", "Hypertension", "Kidney Disease", "Other"]),
            "diet_type": st.multiselect("Diet Type", ["Vegetarian", "Vegan", "Pescatarian", "Halal", "Kosher"])
        })

        col1, col2 = st.columns(2)
        with col1:
            st.button("⬅️ Back", on_click=prev_step)
        with col2:
            st.button("Next ➡️", on_click=next_step)

        if st.button("Generate Diet Plan ✅", key="gen_plan_step2"):
            generate_diet_plan(st.session_state.inputs)

    elif st.session_state.step == 3:
        st.subheader("Cuisine & Food Style")

        st.session_state.inputs.update({
            "cuisines": st.multiselect("Preferred Cuisines",
                                       ["Bangladeshi", "Indian", "Italian", "Chinese", "Japanese", "Mediterranean",
                                        "Middle Eastern", "Other"]),
            "meal_pattern": st.radio("Meal Structure", ["3 Meals a Day", "5-6 Small Meals", "One Main + Light Meals",
                                                        "Intermittent Fasting"])
        })

        st.button("⬅️ Back", on_click=prev_step)
        if st.button("Generate Diet Plan ✅", key="gen_plan_step3"):
            generate_diet_plan(st.session_state.inputs)


if __name__ == "__main__":
    main()
