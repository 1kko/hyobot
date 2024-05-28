import logging


def getDict(
    dictData: dict, keys: list, default=None
) -> dict | str | int | float | None:
    """
    Traverse a nested dictionary structure and retrieve the value specified by a sequence of keys,
    returning a default value if the key path is not found.

    This function iteratively accesses nested dictionaries or lists based on the provided keys.
    If any key in the sequence is not found, the function returns the specified default value.
    It supports accessing nested elements in both dictionaries and lists.

    Args:
        dictData (dict): The dictionary to be traversed.
        keys (list): A list of keys representing the path to the desired value. Each key should be
                     a string if it's for a dictionary, or an integer if it's for a list index.
        default (any, optional): The default value to return if the key path is not found. Defaults to None.

    Returns:
        dict | str | int | float | None: The value found at the specified path, or the default value
                                         if the path is not found. The type of the return value depends
                                         on the content of the nested structure.

    Example:
        data = {"a": {"b": {"c": [1, 2, 3]}}}
        value = getDict(data, ["a", "b", "c", 0])  # Returns 1
        value = getDict(data, ["a", "x", "y"], default="Not Found")  # Returns "Not Found"

    Note:
        This function does not raise exceptions for missing keys or indices; it returns the default value in such cases.
    """
    current_data = dictData
    for key in keys:
        if isinstance(current_data, dict) and key in current_data:
            current_data = current_data[key]
        elif (
            isinstance(current_data, list)
            and isinstance(key, int)
            and key < len(current_data)
        ):
            current_data = current_data[key]
        else:
            return default
    return current_data


formatter = logging.Formatter(
    "[%(asctime)s] [%(process)d] [%(levelname)s] %(filename)s:%(lineno)d :%(funcName)s: %(message)s",
    "%Y-%m-%d %H:%M:%S %z",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
