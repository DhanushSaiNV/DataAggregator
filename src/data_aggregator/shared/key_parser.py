from typing import Any


def parse_keys(data: dict, keys: list[str]) -> dict[str, Any]:
    result = {}

    for key in keys:
        value = _find_in_dict(key, data)
        result[key] = value

    return result


def _find_in_dict(target_key, data):
    for key, value in data.items():
        if key == target_key:
            return value

        if isinstance(value, dict):
            result = _find_in_dict(target_key, value)
            if result is not None:  # Only return if found
                return result

    return None  # Not found
