import os
import base64
import streamlit as st
from PyPDF2 import PdfReader

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Consumption Estimate Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# PLACEHOLDER LLM FUNCTION
# ======================================================
def query_llm(prompt):
    if "connection success" in prompt.lower():
        return "Connection success"
    return {"resources": [], "assumptions": []}

# ======================================================
# LOAD CSS
# ======================================================
def load_css():
    if os.path.exists("style.css"):
        with open("style.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ======================================================
# FIXED BRANDING
# ======================================================
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO_PATH = "./assets/sigmoid-logo.jpeg"
logo_base64 = get_base64_image(LOGO_PATH)

st.markdown(
    f"""
    <div class="fixed-branding">
        <img src="data:image/jpeg;base64,{logo_base64}">
        <div class="brand-text">Powered by <b>Databricks</b></div>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# HERO
# ======================================================
st.markdown(
    """
    <div class="hero-section">
        <h1 class="hero-title">Consumption Estimate Calculator</h1>
        <p class="hero-subtitle-strong">An AI-powered calculator</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:
    st.header("⚙️ User Input")

    client_name = st.text_input("Client Name", placeholder="Acme Corp")
    use_case_name = st.text_input("Use Case Name", placeholder="Annual Budget Planning")

    use_case_type = st.selectbox(
        "Use Case Type",
        ["Select use case", "Data Migration", "Machine Learning", "Reporting"],
        key="use_case_type"
    )

    cloud_options = ["Databricks", "AWS", "Azure"]

    # =========================
    # DATA MIGRATION
    # =========================
    data_migration_inputs = {}

    if use_case_type == "Data Migration":
        st.subheader("📦 Data Migration Inputs")

        cloud_type_dm = st.multiselect(
            "Cloud Type",
            cloud_options,
            key="cloud_type_data_migration"
        )

        migration_type = st.radio(
            "Migration Type",
            ["One-time Historical Load", "Ongoing Incremental", "Both"],
            key="migration_type"
        )

        pipeline_mode = st.radio(
            "Pipeline Mode",
            ["Batch", "Streaming"],
            key="pipeline_mode"
        )

        historical_data_gb = st.number_input(
            "Historical Data Size (GB)", 1, 500000, 1000, key="hist_gb"
        )
        daily_incremental_gb = st.number_input(
            "Daily Incremental Data (GB/day)", 0, 100000, 100, key="daily_gb"
        )

        pipelines_count = st.number_input(
            "Number of Pipelines", 1, 500, 5, key="pipelines_count"
        )
        pipeline_runs_per_day = st.number_input(
            "Pipeline Runs per Day", 1, 48, 1, key="runs_per_day"
        )
        avg_runtime_hours = st.number_input(
            "Avg Runtime per Pipeline (hours)", 0.1, 24.0, 2.0, step=0.1, key="runtime"
        )

        source_systems = st.number_input(
            "Source Systems", 1, 100, 2, key="source_systems"
        )
        destination_systems = st.number_input(
            "Destination Systems", 1, 20, 1, key="destination_systems"
        )

        transformation_complexity = st.selectbox(
            "Transformation Complexity",
            ["Low (Copy)", "Medium (Joins)", "High (Aggregations / Enrichment)"],
            key="transform_complexity"
        )

        concurrent_pipelines = st.number_input(
            "Max Concurrent Pipelines", 1, 100, 3, key="concurrent_pipelines"
        )
        storage_retention_days = st.number_input(
            "Raw Data Retention (days)", 1, 3650, 90, key="retention_days"
        )

        data_migration_inputs = {
            "cloud_type": cloud_type_dm,
            "migration_type": migration_type,
            "pipeline_mode": pipeline_mode,
            "historical_data_gb": historical_data_gb,
            "daily_incremental_gb": daily_incremental_gb,
            "pipelines": pipelines_count,
            "runs_per_day": pipeline_runs_per_day,
            "avg_runtime_hours": avg_runtime_hours,
            "source_systems": source_systems,
            "destination_systems": destination_systems,
            "transformation_complexity": transformation_complexity,
            "concurrent_pipelines": concurrent_pipelines,
            "storage_retention_days": storage_retention_days
        }

    # =========================
    # MACHINE LEARNING
    # =========================
    ml_inputs = {}

    if use_case_type == "Machine Learning":
        st.subheader("🤖 Machine Learning Inputs")

        cloud_type_ml = st.multiselect(
            "Cloud Type",
            cloud_options,
            key="cloud_type_machine_learning"
        )

        workload_types = st.multiselect(
            "Workload Type",
            ["Training", "Batch Inference", "Real-time Inference"],
            key="workload_types"
        )

        training_data_gb = st.number_input(
            "Training Data Size (GB)", 1, 500000, 200, key="training_gb"
        )
        training_frequency = st.selectbox(
            "Training Frequency",
            ["Daily", "Weekly", "Monthly", "On Demand"],
            key="training_frequency"
        )
        avg_training_hours = st.number_input(
            "Avg Training Duration (hours)", 0.5, 168.0, 4.0, step=0.5, key="training_hours"
        )

        models_count = st.number_input(
            "Number of Models", 1, 200, 3, key="models_count"
        )
        inference_requests = st.number_input(
            "Inference Requests per Day", 0, 10000000, 50000, key="inference_requests"
        )
        concurrency = st.number_input(
            "Peak Concurrent Inference Requests", 1, 100000, 100, key="ml_concurrency"
        )

        use_gpu = st.radio("Use GPU?", ["No", "Yes"], key="use_gpu")
        gpu_hours = 0
        if use_gpu == "Yes":
            gpu_hours = st.number_input(
                "GPU Usage (hours/day)", 1, 24, 8, key="gpu_hours"
            )

        model_retention_days = st.number_input(
            "Model Retention (days)", 1, 3650, 180, key="model_retention"
        )

        ml_inputs = {
            "cloud_type": cloud_type_ml,
            "workload_types": workload_types,
            "training_data_gb": training_data_gb,
            "training_frequency": training_frequency,
            "avg_training_hours": avg_training_hours,
            "models_count": models_count,
            "inference_requests_per_day": inference_requests,
            "peak_concurrency": concurrency,
            "use_gpu": use_gpu,
            "gpu_hours_per_day": gpu_hours,
            "model_retention_days": model_retention_days
        }

    # =========================
    # REPORTING
    # =========================
    reporting_inputs = {}

    if use_case_type == "Reporting":
        st.subheader("📊 Reporting Inputs")

        cloud_type_reporting = st.multiselect(
            "Cloud Type",
            cloud_options,
            key="cloud_type_reporting"
        )

        reporting_tool = st.selectbox(
            "Reporting Tool",
            ["Select", "Power BI", "Tableau"],
            key="reporting_tool"
        )

        user_type = None
        number_of_users = None

        if reporting_tool in ["Power BI", "Tableau"]:
            user_type = st.radio(
                "User Type", ["Viewer", "Pro", "Premium"], key="report_user_type"
            )
            number_of_users = st.number_input(
                "Number of Users", 1, 10000, 20, key="report_users"
            )

        reporting_inputs = {
            "cloud_type": cloud_type_reporting,
            "tool": reporting_tool,
            "user_type": user_type,
            "number_of_users": number_of_users
        }

# ======================================================
# STORE CONFIG
# ======================================================
st.session_state.usecase_config = {
    "client_name": client_name,
    "use_case_name": use_case_name,
    "use_case_type": use_case_type,
    "data_migration": data_migration_inputs,
    "machine_learning": ml_inputs,
    "reporting": reporting_inputs
}

# ======================================================
# UPLOAD ARTIFACTS
# ======================================================
st.header("Upload Artifacts")
st.info("Upload PNG, JPG, JPEG, or PDF files.")

uploaded_files = st.file_uploader(
    "Select files",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg", "pdf"]
)

extracted_text = ""

if uploaded_files:
    for file in uploaded_files:
        if file.name.lower().endswith(("png", "jpg", "jpeg")):
            st.image(file, caption=file.name, width=400)
            extracted_text += f"[IMAGE: {file.name}]\n"

        if file.name.lower().endswith("pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

# ======================================================
# AI ANALYSIS
# ======================================================
st.header("AI Analysis & Cost Estimation")

prompt_input = st.text_area(
    "User Prompt",
    "Extract cloud resources and estimate consumption. Output JSON only.",
    height=140
)

st.markdown("---")

col1, col2 = st.columns([3, 1])

with col1:
    if st.button("🚀 Generate Cost Estimate with AI", use_container_width=True, type="primary"):
        cfg = st.session_state.usecase_config

        final_prompt = f"""
CLIENT: {cfg['client_name']}
USE CASE: {cfg['use_case_name']}
TYPE: {cfg['use_case_type']}

DATA MIGRATION INPUTS:
{cfg['data_migration']}

MACHINE LEARNING INPUTS:
{cfg['machine_learning']}

REPORTING INPUTS:
{cfg['reporting']}

USER INSTRUCTION:
{prompt_input}

ARCHITECTURE:
{extracted_text}
"""

        with st.spinner("Analyzing and estimating..."):
            response = query_llm(final_prompt)

        st.subheader("AI Estimated Output")
        st.json(response)

with col2:
    if st.button("🔌 Test LLM", use_container_width=True):
        res = query_llm("connection success")
        if res == "Connection success":
            st.success("LLM Connected")
        else:
            st.error("LLM Connection Failed")