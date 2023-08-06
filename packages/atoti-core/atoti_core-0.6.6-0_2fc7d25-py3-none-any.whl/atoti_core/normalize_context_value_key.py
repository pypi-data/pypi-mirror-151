from typing import Mapping

from .deprecated import deprecated

_DEPRECATED_KEY_TO_NEW_KEY: Mapping[str, str] = {
    "queriesResultLimit.intermediateSize": "queriesResultLimit.intermediateLimit",
    "queriesResultLimit.transientSize": "queriesResultLimit.transientLimit",
}


def normalize_context_value_key(key: str, /) -> str:
    new_key = _DEPRECATED_KEY_TO_NEW_KEY.get(key)
    if new_key is None:
        return key
    deprecated(f"Context value `{key}` has been renamed `{new_key}`.")
    return new_key
