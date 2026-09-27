"""Recursive JSON searches with optional role-based access control."""

from policy import POLICY


def json_search(key, input_object, role=None):
    """Return matching key-value dictionaries, enforcing policy for explicit roles."""
    if role is not None and key in POLICY and role not in POLICY[key]:
        return []

    results = []
    if isinstance(input_object, dict):
        for current_key, value in input_object.items():
            if current_key == key:
                results.append({current_key: value})
            results.extend(json_search(key, value, role=role))
    elif isinstance(input_object, list):
        for item in input_object:
            results.extend(json_search(key, item, role=role))

    return results
