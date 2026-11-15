"""DiScO STU single-user local application."""
import streamlit as st

st.set_page_config(page_title='DiScO STU', page_icon='🐟', layout='wide')
st.title('🪩 DiScO STU')
st.subheader('Semantic Transformation Utility')
st.write('Use **SERA** to record and freeze what you intended to communicate.')
st.write('Use **STU Transform** to run live Adaption experiments from that frozen source.')
st.write('Use **Review** to inspect differences and **Results** to export the complete private evidence ZIP.')
st.caption('Offline fixtures remain available for regression tests. Live inference sends source text to the selected hosted provider.')
st.caption('Local single-user application · Private runtime data stored under ./data/ (gitignored)')
