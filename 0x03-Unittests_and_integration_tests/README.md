

# Unit Testing - `utils.access_nested_map`

This task is part of the **0x03. Unittests and Integration Tests** project.  
The goal is to understand and test the behavior of the `access_nested_map` function defined in `utils.py`.

---

## Description

The `access_nested_map` function retrieves a value from a nested mapping (like a dictionary) following a given path of keys.

Example:

```python
from utils import access_nested_map

nested_map = {"a": {"b": {"c": 1}}}
result = access_nested_map(nested_map, ("a", "b", "c"))
print(result)  # Output: 1

