# app/core/data_cleaning/noise_filter.py

from collections import deque
import math


class MovingAverageFilter:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.values = deque(maxlen=window_size)

    def filter(self, value: float):
        # ⛔ chặn NaN trước khi vào filter
        if value is None or (isinstance(value, float) and math.isnan(value)):
            if len(self.values) == 0:
                return value
            return sum(self.values) / len(self.values)

        self.values.append(value)
        return sum(self.values) / len(self.values)
