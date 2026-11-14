"""Deliberately minimal model-visible export. Never copy the Oracle and delete fields."""
from __future__ import annotations

from .schema import source_fingerprint


def stu_source_packet(oracle: dict) -> dict:
    if oracle.get("status") != "frozen":
        raise ValueError("Source export requires a frozen Oracle.")
    source = oracle["source"]
    text = source["original_text"]
    if source["source_sha256"] != source_fingerprint(text):
        raise ValueError("Source digest mismatch.")
    # New object assembled from a hardcoded allowlist. Do not add explication fields.
    return {
        "packet_type": "stu_source_v0.1",
        "sample_id": oracle["sample_id"],
        "source_sha256": source["source_sha256"],
        "original_text": text,
    }
