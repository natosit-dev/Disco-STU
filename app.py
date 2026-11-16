"""DiScO STU — the four-part human research workflow."""
import streamlit as st

st.set_page_config(page_title='DiScO STU', page_icon='🐟', layout='wide')
st.title('DiScO STU')
st.caption('Experiment 01 · From Meaning to Management')
st.subheader('Write → Explain → Run → Review')
st.write('DiScO examines how an author’s meaning survives structured decomposition '
         'and two reconstructions, including advice for a commercial business.')
st.markdown('**1. Write & Explain · SERA**')
st.write('Create a short original source and independently record what you meant. '
         'An unrestricted explanation is the human reference. Optional characteristics '
         'and advanced structures are never required for new v0.2 records.')
st.markdown('**2. Run · Transform**')
st.write('Freeze the authorial baseline, choose a hosted model, and run one decomposition '
         'followed by neutral and commercial reconstructions. Raw evidence is retained.')
st.markdown('**3. Review**')
st.write('Compare the original writing directly against each final output. '
         'Keep the frozen authorial intention nearby as an optional reference.')
st.markdown('**4. Results**')
st.write('Inspect completion, optional diagnostic comparisons, and export the complete '
         'private evidence bundle.')
with st.expander('Evidence and scientific boundaries'):
    st.write('The software retains original UUIDs, UTC timestamps, frozen Oracles, '
             'provider responses, model-visible projections, hashes, and review events.')
    st.write('Successful API execution does not establish semantic correctness. '
             'Synthetic fixtures are regression tests, not model observations.')
    st.warning('Private research data remain on this local workstation under ./data/. '
               'Do not publish complete private ZIPs without reviewing their contents.')
