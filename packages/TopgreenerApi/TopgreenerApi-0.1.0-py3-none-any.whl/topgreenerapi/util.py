def order_dict(dictionary):
    return {k: order_dict(v) if isinstance(v, dict) else v
            for k, v in sorted(dictionary.items())}


def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min
