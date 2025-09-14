import json, os

_cache = {}

def load_data(filename, default=None):
    global _cache
    if default is None:
        default = []
    # return cached if present
    if filename in _cache:
        return _cache[filename]
    # if file missing -> set default
    if not os.path.exists(filename):
        _cache[filename] = default
        return _cache[filename]
    try:
        with open(filename, "r", encoding="utf-8") as f:
            _cache[filename] = json.load(f)
    except Exception:
        _cache[filename] = default
    return _cache[filename]

def save_data(filename, data=None):
    global _cache
    if data is not None:
        _cache[filename] = data
    if filename not in _cache:
        _cache[filename] = []
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(_cache[filename], f, indent=4, ensure_ascii=False)
