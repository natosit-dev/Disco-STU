"""DiScO STU local application. SERA is implemented; STU execution is not."""
import streamlit as st

st.set_page_config(page_title="DiScO STU", page_icon="🐟", layout="wide")
st.title("🪩 DiScO STU")
st.subheader("Semantic Transformation Utility")
st.write("SERA is the working capture tool: select a paragraph, explain what you meant, structure the meaning, and freeze a reference the models never see.")
st.info("Use **SERA** in the left sidebar. STU model execution and timed human gap review are not implemented in this baseline.")
st.caption("Local single-user application · Runtime records stored under ./data/ (excluded from Git)")
