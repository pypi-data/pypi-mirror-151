import hashlib
import json
from pathlib import Path
from typing import Any, Optional, Union

import cloudpickle


def stable_hash(*args: Union[str, bytes]) -> str:
    """Given some arguments, produces a stable 64-bit hash of their contents.

    Supports bytes and strings. Strings will be UTF-8 encoded.

    Args:
        *args: Items to include in the hash.

    Returns:
        A hex hash.
    """
    h = hashlib.md5()
    for a in args:
        if isinstance(a, str):
            a = a.encode()
        h.update(a)
    return h.hexdigest()


def file_hash(path: str) -> str:
    """Given a path to a file, produces a stable hash of the file contents.

    Args:
        path (str): the path to a file

    Returns:
        str: a hash of the file contents
    """
    contents = Path(path).read_bytes()
    return stable_hash(contents)


def to_qualified_name(obj: Any) -> str:
    """
    Given an object, returns its fully-qualified name, meaning a string that represents its
    Python import path

    Args:
        obj (Any): an importable Python object

    Returns:
        str: the qualified name
    """
    return obj.__module__ + "." + obj.__qualname__


def hash_objects(*args, **kwargs) -> Optional[str]:
    """
    Attempt to hash objects by dumping to JSON or serializing with cloudpickle.
    On failure of both, `None` will be returned
    """
    try:
        return stable_hash(json.dumps((args, kwargs), sort_keys=True))
    except Exception:
        pass

    try:
        return stable_hash(cloudpickle.dumps((args, kwargs)))
    except Exception:
        pass

    return None
