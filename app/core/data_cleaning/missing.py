# app/core/data_cleaning/missing.py

import math

def fill_missing(value, last_value):
    if value is None:
        return last_value

    if isinstance(value, str) and value.lower() == "nan":
        return last_value

    if isinstance(value, float) and math.isnan(value):
        return last_value

    return value
