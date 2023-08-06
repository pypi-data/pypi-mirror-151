import re
from functools import partial


def remove_path_anchor(path):
    """Removes the path anchor, making it a relative path

    Parameters
    ----------
    path : pathlib.Path
        Path from which to strip anchor

    Returns
    -------
    Path
        Relative path
    """
    if path.is_absolute():
        return path.relative_to(path.anchor)
    else:
        return path


def to_snake_case(key):
    """Rewrites a camelCase string in snake_case

    Parameters
    ----------
    key : str
        Key to convert

    Returns
    -------
    str
        Key in snake_case
    """
    return re.sub('([A-Z]+)', r'_\1', key).lower()


def to_camel_case(key):
    """Rewrites a snake_case string in camelCase

    Parameters
    ----------
    key : str
        Key to convert

    Returns
    -------
    str
        Key in camelCase
    """
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), key)


def _rename_key(key, key_map={}):
    return key_map.get(key, key)


def _apply_key_funcs(key, funcs):
    for func in funcs:
        key = func(key)
    return key


def recursively_map_dict_keys(obj, func):
    """Recursively traverse dicts or lists of dicts to apply a function to each dictionary key

    Parameters
    ----------
    obj : dict or list
        Object to traverse
    func : function
        Function to apply to dictionary keys

    Returns
    -------
    dict
        Dictionary with keys modified by `func`
    """
    if isinstance(obj, dict):  # if dict, apply to each key
        return {func(k): recursively_map_dict_keys(v, func) for k, v in obj.items()}
    elif isinstance(obj, list):  # if list, apply to each element
        return [recursively_map_dict_keys(elem, func) for elem in obj]
    else:
        return obj


def rename_dict_keys(input_dict, key_map):
    """Renames the keys in a dictionary

    Parameters
    ----------
    input_dict : dict
        Dictionary for which to change the keys
    key_map : dict
        Dictionary which specifies old keys to be swapped with new keys in the input_dict, e.g `{'old_key': 'new_key'}`

    Returns
    -------
    dict
        Copy of `input_dict` with old keys subbed for new keys
    """
    funcs = [partial(_rename_key, key_map=key_map)]
    return recursively_map_dict_keys(input_dict, partial(_apply_key_funcs, funcs=funcs))


def convert_dict_keys(input_dict, key_map={}, reverse=False):
    """Convert the keys of a dictionary from camelCase to snake_case

    Parameters
    ----------
    input_dict : dict
        Dictionary for which to convert the keys
    key_map : dict, optional
        Dictionary which specifies old keys to be swapped with new keys in `input_dict`,
        e.g `{'old_key': 'new_key'}`, by default {}
    reverse : bool, optional
        If True, will return snake_case keys to camelCase, by default False

    Returns
    -------
    dict
        Copy of `input_dict` with keys converted from camelCase to snake_case, and optional other key sets exchanged
    """
    funcs = []
    if key_map:
        funcs.append(partial(_rename_key, key_map=key_map))

    funcs.append(to_camel_case if reverse else to_snake_case)

    return recursively_map_dict_keys(input_dict, partial(_apply_key_funcs, funcs=funcs))
