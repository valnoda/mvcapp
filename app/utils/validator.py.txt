import re
from app.exceptions.custom_exceptions import ValidationError

def validate_input(key1, key2):
    pattern = r'^[a-zA-Z]{3}\d{1,5}$'  # 3文字の英字 + 1~5桁の数字

    if not re.match(pattern, key1):
        raise ValidationError("リクエストデータが不正です", errors={"key1": "Invalid format"})
    if not re.match(pattern, key2):
        raise ValidationError("リクエストデータが不正です", errors={"key2": "Invalid format"})

# def validate_input(key1, key2):
#     if not (isinstance(key1, str) and len(key1) == 4):
#         # raise ValueError("Invalid key1")
#         raise ValidationError("リクエストデータが不正です", errors={"key1": "Invalid"})
#     if not (isinstance(key2, str) and len(key2) == 4):
#         # raise ValueError("Invalid key2")
#         raise ValidationError("リクエストデータが不正です", errors={"key2": "Invalid"})