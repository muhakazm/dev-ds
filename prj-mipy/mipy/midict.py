#[BEGIN][textdicts]

class InsensitiveKeysDict(dict):
    """
    A dictionary that allows case-insensitive key lookups while preserving the original casing.

    Example:
        >>> d = InsensitiveKeysDict({"Hello": "World", "TEST": 123})
        >>> print(d["hello"])  # Output: World
        >>> print(d["test"])  # Output: 123
        >>> d["hElLo"] = "New Value"
        >>> print(d)  # Output: {'Hello': 'New Value', 'TEST': 123}
        >>> print(d.to_dict())  # Output: {'Hello': 'New Value', 'TEST': 123}
    """
    def __init__(self, data=None, **kwargs):
        super().__init__()
        self._key_map = {}  # Stores lowercase -> original key mapping
        if data:
            self.update(data)
        if kwargs:
            self.update(kwargs)

    def __setitem__(self, key, value):
        if isinstance(key, str):
            lower_key = key.lower()
            if lower_key in self._key_map:
                original_key = self._key_map[lower_key]
                super().__delitem__(original_key)  # Remove old key
            self._key_map[lower_key] = key  # Store new key mapping
        super().__setitem__(key, value)

    def __getitem__(self, key):
        if isinstance(key, str):
            key = self._key_map.get(key.lower(), key)  # Use original key
        return super().__getitem__(key)

    def __delitem__(self, key):
        if isinstance(key, str):
            key = self._key_map.pop(key.lower(), key)  # Remove from map
        super().__delitem__(key)

    def get(self, key, default=None):
        if isinstance(key, str):
            key = self._key_map.get(key.lower(), key)
        return super().get(key, default)

    def __contains__(self, key):
        if isinstance(key, str):
            return key.lower() in self._key_map
        return super().__contains__(key)

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).items():
            self[key] = value

    def pop(self, key, default=None):
        if isinstance(key, str):
            key = self._key_map.pop(key.lower(), key)
        return super().pop(key, default)

    def setdefault(self, key, default=None):
        if isinstance(key, str):
            key = self._key_map.get(key.lower(), key)
        return super().setdefault(key, default)

    def to_dict(self):
        """Convert to a standard dictionary (useful for JSON serialization)."""
        return dict(self)

class DeepInsensitiveKeysDict(InsensitiveKeysDict):
    """
    A case-insensitive dictionary that also applies to nested dictionaries.
    
    Example:
        >>> d = DeepInsensitiveKeysDict({"Outer": {"Inner": "Value"}})
        >>> print(d["outer"]["inner"])  # Output: Value
    """
    def __setitem__(self, key, value):
        if isinstance(value, dict):  # Convert nested dicts
            value = DeepInsensitiveKeysDict(value)
        super().__setitem__(key, value)

#[END][textdicts]