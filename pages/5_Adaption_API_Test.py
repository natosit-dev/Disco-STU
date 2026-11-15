"""A minimal one-call hosted inference diagnostic; no experiment or file writes."""
from __future__ import annotations

import os
import streamlit as st

from stu.adaption_api import (AdaptionApiError, AdaptionDiagnosticService,
                              DIAGNOSTIC_PROMPT, SUPPORTED_MODELS)
from ui.adaption_credentials import render_api_key_input

st.set_page_config(page_title='Adaption API Test · DiScO STU', layout='wide')
st.title('Adaption API Test')
st.caption('Send one minimal hosted inference request before enabling live STU experiments.')

with st.expander('API credential', expanded=True):
    key = render_api_key_input()

model = st.selectbox('Hosted model', SUPPORTED_MODELS, index=0)
st.code(DIAGNOSTIC_PROMPT, language=None)
st.caption('One potentially billable request. No tools, memory, or conversation history; no data is saved.')
if st.button('Send one API test request', type='primary', disabled=not (key or os.environ.get('ADAPTION_API_KEY'))):
    try:
        with st.spinner('Calling Adaption once...'):
            result = AdaptionDiagnosticService().test(model, api_key=key)
        if result['ok']:
            st.success('Provider returned a completed, nonempty response.')
        else:
            st.warning('The provider did not return a completed, nonempty response.')
        st.markdown('**Model output**')
        st.code(result['output_text'] or '(empty)', language=None)
        st.markdown('**Request / response metadata**')
        st.json({k: v for k, v in result.items() if k != 'output_text'})
        if result['output_text'].strip() != 'OK':
            st.info('The output differs from OK. Connectivity may still be successful; this is not a semantic evaluation.')
    except AdaptionApiError as exc:
        st.error(str(exc))
