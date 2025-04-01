import math


def sanitize_floats(obj):
    if isinstance(obj, float):
        if math.isinf(obj):
            return "Infinity"  # 或 None / 字符串标记
        elif math.isnan(obj):
            return "NaN"
    elif isinstance(obj, dict):
        return {k: sanitize_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_floats(v) for v in obj]
    return obj


