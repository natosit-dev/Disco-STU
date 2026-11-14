import json
from pathlib import Path

import jsonschema

from sera.schema import CATEGORIES, RELATION_TYPES, UNIT_KINDS
from tests.test_sera import ready_record


def test_shared_semantic_json_schema():
    path = Path(__file__).parents[1] / "schemas" / "semantic_v0.1.json"
    schema = json.loads(path.read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    rec = ready_record()
    payload = {name: rec[name] for name in ("category_prose", "units", "relations")}
    jsonschema.validate(payload, schema)
    assert set(schema["properties"]["category_prose"]["properties"]) == set(CATEGORIES)
    assert set(schema["properties"]["units"]["items"]["properties"]["kind"]["enum"]) == set(UNIT_KINDS)
    assert set(schema["properties"]["relations"]["items"]["properties"]["relation_type"]["enum"]) == set(RELATION_TYPES)
