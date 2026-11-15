"""Masked Streamlit input; copy the value to a non-widget session key across pages.

Streamlit cleans up widget keys when navigating between pages, so the separate
session key is essential. Credentials are never stored on disk or in the URL.
"""
from __future__ import annotations

import os
import streamlit as st

SESSION_KEY = '_disco_adaption_api_key'
WIDGET_KEY = '_disco_adaption_api_key_widget'


def _remember() -> None:
    st.session_state[SESSION_KEY] = st.session_state.get(WIDGET_KEY, '').strip()


def _clear() -> None:
    st.session_state[SESSION_KEY] = ''
    st.session_state[WIDGET_KEY] = ''


def render_api_key_input() -> str | None:
    """Return ephemeral credential for backend; session value overrides environment."""
    if WIDGET_KEY not in st.session_state:
        st.session_state[WIDGET_KEY] = st.session_state.get(SESSION_KEY, '')
    st.text_input(
        'Adaption API key', type='password', key=WIDGET_KEY, on_change=_remember,
        help='Kept only in this running Streamlit session. Never saved to studies or ZIPs.',
        placeholder='Paste API key (or use ADAPTION_API_KEY)',
    )
    st.button('Clear session key', on_click=_clear, key='clear_adaption_session_key')
    session_key = st.session_state.get(SESSION_KEY) or ''
    env_present = bool(os.environ.get('ADAPTION_API_KEY'))
    if session_key:
        st.caption('Session key configured. Only this local Streamlit session can use it.')
    elif env_present:
        st.caption('Using ADAPTION_API_KEY from the server environment.')
    else:
        st.caption('No key configured. Paste one above to test Adaption.')
    return session_key or None
