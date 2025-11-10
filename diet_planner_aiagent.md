# AI Agent - Diet Planner
This is an AI agent that can suggest a diet plan based on user input such as age, weight, height, activity level, and dietary preferences.

### How to run:
1. Authenticate to gcloud:
```shell
gcloud auth application-default login
```
2. Run the streamlit app. It includes a simple UI wizard to collect user inputs and display the diet plan.
```shell
streamlit run aiagents/src/diet_wizard.py
```
Upon successful execution, it starts a local web server and provides a URL (usually http://localhost:8501) to access the app in your web browser.