# app/core/data_cleaning/outlier.py

def remove_outlier(value, min_val, max_val, last_valid):
    """
    Nếu vượt ngưỡng -> dùng giá trị hợp lệ trước đó
    """
    if value < min_val or value > max_val:
        return last_valid
    return value
