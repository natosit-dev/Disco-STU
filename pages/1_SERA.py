"""Progressive, human-only semantic explication. Persistent changes require explicit clicks."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd
import streamlit as st

from sera import CATEGORIES, SeraStore, new_record, validate_freeze
from sera.schema import DOMAINS, IMPORTANCE, POLARITY, RELATION_TYPES, UNIT_KINDS
from sera.service import save_category_prose, save_intention, save_relations, save_units, update_source

st.set_page_config(page_title="SERA · DiScO STU", page_icon="🐟", layout="wide")
st.title("🐟 SERA")
st.caption("Semantic Explication Recorded Analytics · Your meaning first, before the model sees the paragraph")
st.markdown("**Progressive explication:** source → unrestricted intention → category prose → semantic units and relations → frozen Oracle.")

store = SeraStore(os.environ.get("SERA_DATA_DIR", "data"))


def save_and_rerun(record: dict, event: str) -> None:
    try:
        store.save_draft(record, event=event)
    except Exception as exc:
        st.error(f"Save failed: {exc}")
        st.stop()
    st.rerun()


def record_json(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def edited_rows(frame: pd.DataFrame) -> list[dict]:
    return frame.where(pd.notna(frame), "").to_dict(orient="records")


sample_ids = store.sample_ids()
options = ["Create a new sample", *sample_ids]
focus = st.session_state.pop("_focus_sample", None)
if focus in options:
    st.session_state["sample_selection"] = focus
with st.sidebar:
    st.header("Samples")
    choice = st.selectbox("Select sample", options, key="sample_selection")
    st.caption("Single-user local storage. Frozen Oracle records are never sent to a model.")
    st.caption(f"Data directory: {store.root}")

if choice == "Create a new sample":
    st.subheader("1 · Capture a paragraph")
    with st.form("new_source", clear_on_submit=False):
        text = st.text_area("Original paragraph (up to 200 words)", height=210,
                            help="One contiguous paragraph. No auto-truncation or semantic preprocessing.")
        title = st.text_input("Source title / identifier")
        origin = st.text_input("Source location / citation (optional)")
        original_date = st.text_input("Original date (if known)")
        domain = st.selectbox("Domain", DOMAINS, index=4)
        dependencies = st.text_area("Context dependencies (private; not passed to STU)", height=100)
        submitted = st.form_submit_button("Create local SERA draft", type="primary")
    if submitted:
        try:
            record = new_record(text, title, origin, original_date, domain, dependencies)
            store.save_draft(record, event="source_created")
            st.session_state["_focus_sample"] = record["sample_id"]
            st.rerun()
        except Exception as exc:
            st.error(str(exc))
    st.stop()

try:
    record = store.load(choice)
except Exception as exc:
    st.error(f"Cannot load this sample: {exc}")
    st.stop()

st.subheader(record["source"].get("title") or f"Sample {record['sample_id'][:8]}")
st.caption(f"Sample {record['sample_id']} · Explication {record['explication_id']} · Version {record['version']} · {record['status'].upper()}")

if record["status"] == "frozen":
    st.success("Frozen Oracle reference · read only")
    st.markdown("**Original paragraph**")
    st.write(record["source"]["original_text"])
    st.markdown("**Your unrestricted intended meaning**")
    st.write(record["intention_free_text"])
    with st.expander("Category prose", expanded=False):
        for key, question in CATEGORIES.items():
            st.markdown(f"**{question}**")
            st.write(record["category_prose"].get(key) or "—")
    with st.expander("Structured semantic representation", expanded=False):
        st.write("Units")
        st.dataframe(record["units"], hide_index=True, use_container_width=True)
        st.write("Directed relationships")
        st.dataframe(record["relations"], hide_index=True, use_container_width=True)
    st.download_button("Download PRIVATE Oracle (JSON)", record_json(record),
                       file_name=f"sera-oracle-{choice}-v{record['version']}.json", mime="application/json")
    try:
        packet = store.model_packet(choice)
    except Exception as exc:
        st.error(f"STU export integrity error: {exc}")
    else:
        st.download_button("Download STU source-only packet (JSON)", record_json(packet),
                           file_name=f"stu-source-{choice}.json", mime="application/json")
        st.caption("STU packet contains only original_text, sample_id, source_sha256, and packet_type.")
    if st.button("Begin an amendment (new version)"):
        try:
            store.begin_amendment(choice)
            st.rerun()
        except Exception as exc:
            st.error(f"Cannot begin amendment: {exc}")
    st.stop()

# Stage 1: Capture source; source content becomes locked once free intention is saved.
st.markdown("### 1 · Source")
with st.form("source_edit"):
    text = st.text_area("Original paragraph", value=record["source"]["original_text"],
                        height=150, disabled=bool(record.get("intention_saved_at")))
    title = st.text_input("Title", value=record["source"].get("title", ""))
    origin = st.text_input("Citation / origin", value=record["source"].get("origin", ""))
    original_date = st.text_input("Original date", value=record["source"].get("original_date", ""))
    domain = st.selectbox("Domain", DOMAINS,
                          index=DOMAINS.index(record["source"].get("domain", "other")))
    context_dependencies = st.text_area("Private context dependencies", value=record["source"].get("context_dependencies", ""))
    st.caption(f"{record['source']['word_count']} words · source SHA-256: {record['source']['source_sha256'][:18]}…")
    if st.form_submit_button("Save source / provenance"):
        try:
            update_source(record, original_text=text, title=title, origin=origin,
                          original_date=original_date, domain=domain,
                          context_dependencies=context_dependencies)
            save_and_rerun(record, "source_saved")
        except Exception as exc:
            st.error(str(exc))

# Stage 2: Save unrestricted intention BEFORE category structure is shown.
st.markdown("### 2 · What did you intend to communicate?")
st.caption("Unrestricted human explication. Write this before the category questions are revealed. No word limit.")
with st.form("free_intention"):
    intention = st.text_area("Your intended meaning", value=record.get("intention_free_text", ""), height=220)
    if st.form_submit_button("Save unrestricted intention", type="primary" if not record.get("intention_saved_at") else "secondary"):
        try:
            save_intention(record, intention)
            save_and_rerun(record, "intention_saved")
        except Exception as exc:
            st.error(str(exc))

if not record.get("intention_saved_at"):
    st.info("Save your unrestricted intention to unlock category-level explication.")
    st.stop()

# Stage 3: Save category-level prose BEFORE structure is shown.
st.markdown("### 3 · Explain the categories in prose")
st.caption("Empty categories are valid. Describe relationships in your own language before translating them into structured records.")
with st.form("category_prose"):
    prose = {key: st.text_area(question, value=record["category_prose"].get(key, ""),
                               height=90, key=f"category-{key}-{record['explication_id']}")
             for key, question in CATEGORIES.items()}
    if st.form_submit_button("Save category-level prose", type="primary" if not record.get("categories_saved_at") else "secondary"):
        try:
            save_category_prose(record, prose)
            save_and_rerun(record, "categories_saved")
        except Exception as exc:
            st.error(str(exc))

if not record.get("categories_saved_at"):
    st.info("Save the category prose (even if some fields are blank) to unlock structured units and relationships.")
    st.stop()

# Stage 4: Human assigns units and relationships. The table may be empty until saved.
st.markdown("### 4 · Semantic units")
st.caption("One row per claim, actor, negation, condition, etc. IDs are generated on save; existing IDs remain stable.")
unit_cols = ["unit_id", "kind", "text", "importance", "polarity", "source_support", "notes"]
with st.form("semantic_units"):
    units_df = pd.DataFrame(record["units"], columns=unit_cols).fillna("")
    edited_units = st.data_editor(
        units_df, num_rows="dynamic", hide_index=True, use_container_width=True,
        column_config={
            "unit_id": st.column_config.TextColumn("Unit ID (blank = auto)"),
            "kind": st.column_config.SelectboxColumn("Kind", options=list(UNIT_KINDS)),
            "text": st.column_config.TextColumn("Meaning / claim", width="large"),
            "importance": st.column_config.SelectboxColumn("Importance", options=list(IMPORTANCE)),
            "polarity": st.column_config.SelectboxColumn("Polarity", options=list(POLARITY)),
            "source_support": st.column_config.TextColumn("Source support (optional)"),
            "notes": st.column_config.TextColumn("Notes (optional)"),
        }, key=f"units-{record['explication_id']}")
    if st.form_submit_button("Save semantic units"):
        try:
            save_units(record, edited_rows(edited_units))
            save_and_rerun(record, "units_saved")
        except Exception as exc:
            st.error(str(exc))

st.markdown("### 4b · Relationships between units")
st.caption("Save units first, then refer to their IDs. Relations are directed: FROM → TO. 'other' requires an explanation.")
relation_cols = ["relation_id", "from_unit_id", "relation_type", "to_unit_id", "explanation"]
unit_ids = [u["unit_id"] for u in record["units"]]
if unit_ids:
    st.caption("Available unit IDs: " + ", ".join(unit_ids))
with st.form("semantic_relations"):
    relations_df = pd.DataFrame(record["relations"], columns=relation_cols).fillna("")
    edited_relations = st.data_editor(
        relations_df, num_rows="dynamic", hide_index=True, use_container_width=True,
        column_config={
            "relation_id": st.column_config.TextColumn("Relation ID (blank = auto)"),
            "from_unit_id": st.column_config.SelectboxColumn("From unit", options=unit_ids),
            "relation_type": st.column_config.SelectboxColumn("Relation", options=list(RELATION_TYPES)),
            "to_unit_id": st.column_config.SelectboxColumn("To unit", options=unit_ids),
            "explanation": st.column_config.TextColumn("Explanation / custom relation", width="large"),
        }, key=f"relations-{record['explication_id']}")
    if st.form_submit_button("Save relationships"):
        try:
            save_relations(record, edited_rows(edited_relations))
            save_and_rerun(record, "relations_saved")
        except Exception as exc:
            st.error(str(exc))

st.markdown("### 5 · Review, freeze, and export")
with st.expander("Inspect full draft JSON", expanded=False):
    st.json(record)
errors = validate_freeze(record)
if errors:
    for error in errors:
        st.warning(error)
else:
    st.success("Draft passes structural validation. Freezing will create a private Oracle and a separate allowlisted STU packet.")
with st.form("freeze_confirmation"):
    confirmed = st.checkbox("I have reviewed this record. Freeze the current version and keep it immutable.")
    clicked = st.form_submit_button("Freeze Oracle reference", type="primary", disabled=bool(errors))
    if clicked:
        if not confirmed:
            st.error("Confirm freeze explicitly before continuing.")
        else:
            try:
                store.freeze(record)
                st.rerun()
            except Exception as exc:
                st.error(f"Freeze failed: {exc}")
