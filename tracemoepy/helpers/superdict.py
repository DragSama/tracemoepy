import json

from typing import Tuple, List, Set, Union, Dict, Any

class SuperDict(dict):
    """
    Custom dict to access dict keys as attributes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self) -> Dict[str, Any]:
        "Convert SuperDict back to dict."
        _dict = dict(self)
        for key in _dict:
            if isinstance(_dict[key], SuperDict):
                _dict[key] = _dict[key].to_dict()
            elif isinstance(_dict[key], (list, tuple, set)):
                new_list = []
                for i in _dict[key]:
                    if isinstance(i, SuperDict):
                        new_list.append(i.to_dict())
                    else:
                        new_list.append(i)
                _dict[key] = new_list
        return _dict

    def prettify(self, indent=4) -> str:
        """
        Shortuct for `json.dumps(output.to_dict(), indent = 4, ensure_ascii = False)`
        """
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii = False)

    def __getattr__(self, attr):
        return self[attr]


def convert_list(n: Union[List[Any], Tuple[Any, ...], Set[Any]]) -> List[Any]:
    "Helper function for convert()"
    new_list = []
    for item in n:
        if isinstance(item, (list, tuple, set)):
            new_list.append(convert_list(item))
        elif isinstance(item, dict):
            new_list.append(convert(item))
        else:
            new_list.append(item)
    return new_list


def convert(n: dict) -> SuperDict:
    """
    Convert normal dict to SuperDict, So you can access dict keys as attributes.
    Can also convert nested structures.

    Example:
        >>> resp = {"quota": 100}
        >>> resp = convert(resp)
        >>> resp.quota
        100
        >>> resp["quota"]
        100
        >>> nested_resp = {"quota": {"limit": 100, "expires_at": 12345}}
        >>> nested_resp = convert(nested_resp)
        >>> nested_resp.quota.limit
        100
        >>> nested_resp.quota.expires_at
        12345
        >>> complex_nested_resp = {"data": {"results": [{"name": "something"}, {"name": "anything"}]}}
        >>> complex_nested_resp = convert(complex_nested_resp)
        >>> complex_nested_resp.data.results[0].name
        something
    """
    for key in n.keys():
        if isinstance(n[key], dict):
            n[key] = convert(n[key])
        elif isinstance(n[key], (list, tuple, set)):
            n[key] = convert_list(n[key])
    return SuperDict(**n)
