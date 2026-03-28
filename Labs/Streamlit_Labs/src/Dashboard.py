import json
import requests
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
from streamlit.logger import get_logger

# If you start the fast api server on a different port
# make sure to change the port below
FASTAPI_BACKEND_ENDPOINT = "http://localhost:8000"

# Make sure you have the trained model file in FastAPI_Labs/model folder.
# If it's missing run train.py in FastAPI_Labs/src folder
FASTAPI_MODEL_LOCATION = Path(__file__).resolve().parents[2] / 'FastAPI_Labs' / 'model' / 'iris_model.pkl'

# streamlit logger
LOGGER = get_logger(__name__)

# Feature definitions with slider configs: (label, min, max, default, step, type)
HEART_FEATURES = {
    "age":      ("Age (years)", 20, 100, 50, 1, "int"),
    "sex":      ("Sex (0=Female, 1=Male)", 0, 1, 1, 1, "int"),
    "cp":       ("Chest Pain Type (0-3)", 0, 3, 0, 1, "int"),
    "trestbps": ("Resting Blood Pressure (mm Hg)", 80, 200, 120, 1, "int"),
    "chol":     ("Cholesterol (mg/dl)", 100, 600, 200, 1, "int"),
    "fbs":      ("Fasting Blood Sugar > 120 (0=No, 1=Yes)", 0, 1, 0, 1, "int"),
    "restecg":  ("Resting ECG (0-2)", 0, 2, 0, 1, "int"),
    "thalach":  ("Max Heart Rate", 60, 220, 150, 1, "int"),
    "exang":    ("Exercise Induced Angina (0=No, 1=Yes)", 0, 1, 0, 1, "int"),
    "oldpeak":  ("ST Depression (Oldpeak)", 0.0, 7.0, 1.0, 0.1, "float"),
    "slope":    ("Slope of Peak ST Segment (0-2)", 0, 2, 1, 1, "int"),
    "ca":       ("Number of Major Vessels (0-4)", 0, 4, 0, 1, "int"),
    "thal":     ("Thalassemia (0-3)", 0, 3, 2, 1, "int"),
}


def build_feature_radar_chart(values):
    """Create a radar chart showing input feature values normalized to their ranges."""
    labels = [HEART_FEATURES[k][0] for k in HEART_FEATURES]
    mins = [HEART_FEATURES[k][1] for k in HEART_FEATURES]
    maxs = [HEART_FEATURES[k][2] for k in HEART_FEATURES]

    normalized = []
    for key, mn, mx in zip(HEART_FEATURES.keys(), mins, maxs):
        rng = mx - mn if mx - mn != 0 else 1
        normalized.append((values[key] - mn) / rng)

    # Close the radar
    normalized.append(normalized[0])
    labels.append(labels[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=normalized,
        theta=labels,
        fill='toself',
        name='Input Features',
        fillcolor='rgba(78, 205, 196, 0.3)',
        line=dict(color='#4ECDC4', width=2)
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        title="Feature Profile (Normalized)",
        height=450,
        margin=dict(t=60, b=30, l=80, r=80)
    )
    return fig


def build_prediction_card(has_heart_disease):
    """Display a styled prediction result card."""
    if has_heart_disease:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FF6B6B22, #FF6B6B44);
            border-left: 5px solid #FF6B6B;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
        ">
            <h2 style="margin:0;">⚠️ Heart Disease Detected</h2>
            <p style="margin-top:10px; font-size:16px;">
                The model predicts that the patient <strong>may have heart disease</strong>.
                Please consult a medical professional for proper diagnosis.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #4ECDC422, #4ECDC444);
            border-left: 5px solid #4ECDC4;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
        ">
            <h2 style="margin:0;">✅ No Heart Disease Detected</h2>
            <p style="margin-top:10px; font-size:16px;">
                The model predicts that the patient <strong>likely does not have heart disease</strong>.
                Regular checkups are still recommended.
            </p>
        </div>
        """, unsafe_allow_html=True)


def run():
    st.set_page_config(
        page_title="Heart Disease Prediction Demo",
        page_icon="❤️",
    )

    # Build the sidebar
    with st.sidebar:
        # Check the status of backend
        try:
            backend_request = requests.get(FASTAPI_BACKEND_ENDPOINT)
            if backend_request.status_code == 200:
                st.success("Backend online ✅")
            else:
                st.warning("Problem connecting 😭")
        except requests.ConnectionError as ce:
            LOGGER.error(ce)
            LOGGER.error("Backend offline 😱")
            st.error("Backend offline 😱")

        st.info("Configure parameters")

        # --- Input method toggle ---
        input_method = st.radio("Input method", ["Sliders", "JSON File Upload"], horizontal=True)

        if input_method == "Sliders":
            slider_values = {}
            for key, (label, mn, mx, default, step, dtype) in HEART_FEATURES.items():
                if dtype == "float":
                    slider_values[key] = st.slider(label, float(mn), float(mx), float(default), float(step), format="%f")
                else:
                    slider_values[key] = st.slider(label, mn, mx, default, step)

            st.session_state["INPUT_METHOD"] = "sliders"
            st.session_state["slider_values"] = slider_values
            st.session_state["IS_INPUT_READY"] = True

        else:
            test_input_file = st.file_uploader('Upload test prediction file', type=['json'])
            if test_input_file:
                st.write('Preview file')
                test_input_data = json.load(test_input_file)
                st.json(test_input_data)
                st.session_state["INPUT_METHOD"] = "json"
                st.session_state["json_data"] = test_input_data
                st.session_state["IS_INPUT_READY"] = True
            else:
                st.session_state["IS_INPUT_READY"] = False

        predict_button = st.button('Predict', type='primary', use_container_width=True)

    # Dashboard body
    st.write("# Heart Disease Prediction ❤️")
    st.markdown("Predict whether a patient has heart disease based on clinical features.")

    if predict_button:
        if not st.session_state.get("IS_INPUT_READY", False):
            st.toast(':red[Please provide input — use sliders or upload a JSON file.]')
            st.stop()

        # Build client input based on selected method
        if st.session_state.get("INPUT_METHOD") == "sliders":
            values = st.session_state["slider_values"]
        else:
            json_data = st.session_state["json_data"]
            # Support both {"input_test": {...}} and flat {...} formats
            values = json_data.get("input_test", json_data)

        client_input = json.dumps(values)

        try:
            with st.spinner('Predicting...'):
                predict_response = requests.post(
                    f'{FASTAPI_BACKEND_ENDPOINT}/predict', client_input
                )

            if predict_response.status_code == 200:
                result = predict_response.json()
                has_disease = result["has_heart_disease"]

                # --- Prediction result card ---
                build_prediction_card(has_disease)

                # --- Visualizations ---
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Feature Profile")
                    fig = build_feature_radar_chart(values)
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.subheader("Input Values")
                    table_rows = ""
                    for key, (label, *_) in HEART_FEATURES.items():
                        table_rows += f"| {label} | `{values[key]}` |\n"
                    st.markdown(f"""
| Feature | Value |
|---|---|
{table_rows}""")

            else:
                st.toast(
                    f':red[Status from server: {predict_response.status_code}. Refresh page and check backend status]',
                    icon="🔴"
                )
        except Exception as e:
            st.toast(':red[Problem with backend. Refresh page and check backend status]', icon="🔴")
            LOGGER.error(e)


if __name__ == "__main__":
    run()