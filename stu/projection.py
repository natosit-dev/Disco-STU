"""Versioned model-visible reconstruction projection. Full decomposition stays intact."""
from __future__ import annotations

from .contracts import canonical, clean_semantics

PROJECTION_VERSION = 'reconstruction.v0.1'


def projection_bytes(decomposition: dict) -> bytes:
    """Serialize the exact same projection once for both live reconstruction calls."""
    parsed = clean_semantics(decomposition)
    result = {
        'projection_version': PROJECTION_VERSION,
        'category_prose': parsed['category_prose'],
        'units': [{k: v for k, v in unit.items() if k != 'source_support'}
                  for unit in parsed['units']],
        'relations': parsed['relations'],
    }
    payload = canonical(result)
    if b'"source_support"' in payload:
        raise ValueError('Reconstruction projection includes source_support.')
    return payload
