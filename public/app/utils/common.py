import json
from datetime import datetime

def to_json(data):
    """
    JSONに変換する共通関数
    """
    if isinstance(data, dict):
        return json.dumps(data, default=json_default, ensure_ascii=False)
    return json.dumps(data, default=json_default, ensure_ascii=False)

def print_type(obj):
    """
    オブジェクトの型を表示する共通関数
    """
    if isinstance(obj, dict):
        print("Type: dict")
        for key, value in obj.items():
            print(f"Key: {key}, Type of value: {type(value).__name__}")
    elif isinstance(obj, list):
        print("Type: list")
        for item in obj:
            print(f"Type of item: {type(item).__name__}")
    else:
        print(f"Type: {type(obj).__name__}")
    print(f"Type of object: {type(obj).__name__}")

def json_default(obj):
    """
    JSON非対応型が来た場合は対応型に変換する共通関数
    """
    if isinstance(obj, datetime):
        return obj.isoformat()  # 日付をISO8601文字列に変換
    elif isinstance(obj, set):
        return list(obj)  # setはリストに変換
    elif isinstance(obj, Decimal):
        return float(obj)  # Decimalはfloatに変換
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')  # bytesはUTF-8文字列に変換
    else:
        return str(obj)  # その他は文字列化

def fetchall_as_dict(cursor):
    """
    カーソルの結果を「カラム名: 値」の辞書のリストに変換する共通関数
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def to_dict_if_possible(obj):
    """
    コレクション型を判別しdictに変換するメソッド共通関数
    """
    if isinstance(obj, dict):
        return obj
    elif isinstance(obj, list):
        # list of 2-element tuple or list
        try:
            return dict(obj)
        except (TypeError, ValueError):
            print("Cannot convert list elements to dict (must be 2-element pairs)")
            return None
    else:
        print(f"Unsupported type: {type(obj).__name__}")
        return None