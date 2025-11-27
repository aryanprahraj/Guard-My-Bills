import math

def sanitize(value):
    if value is None:
        return 0.0
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return 0.0
    return value

def sanitize_dict(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            clean[k] = sanitize_dict(v)
        elif isinstance(v, list):
            clean[k] = [sanitize_dict(i) if isinstance(i, dict) else sanitize(i) for i in v]
        else:
            clean[k] = sanitize(v)
    return clean
