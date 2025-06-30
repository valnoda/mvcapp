from app.utils.logger import get_logger  # ロガーをインポート
from app.utils.common import to_json  # json形式に変換
import app.config.constants as CONST

class BaseClass:
    def __init__(self, context=None):
        self.context = context
        request_id = getattr(context, "aws_request_id", "-") if context else "-"
        self.logger = get_logger(request_id)

    # 現状利用していないがrequest_idを書き換えてログに出したい場合などに利用
    def set_context(self, request_id):
        self.logger = get_logger(request_id)

    def build_response(self, status=0, message="", data=None, errors=None, status_code=200):
        body = {
            "status": status,
            "message": message,
            "data": data if data is not None else {},
            "errors": errors if errors is not None else {},
        }
    
        return {
            "statusCode": status_code,
            "body": to_json(body),
            "headers": {"Content-Type": "application/json"}
        }