import logging
from app.config.settings import LOG_LEVEL
from app.config.constants import LOG_FORMATTER

class SafeFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "user_id"):
            record.user_id = "unknown"
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return super().format(record)

class RequestLoggerAdapter(logging.LoggerAdapter):
    # logger.info()などが実行されたタイミングで自動で呼ばれるメソッド
    def process(self, msg, kwargs):
        # ベースコンテキストを複製（デフォルトのextra情報上書き防止）
        extra = self.extra.copy()

        # kwargsに extra が指定されていれば、それを上書き
        if "extra" in kwargs:
            extra.update(kwargs["extra"])

        # デフォルトextraの補完
        extra.setdefault("request_id", "-")
        extra.setdefault("user_id", "unknown")

        # 更新したextraをkwargsに戻す
        kwargs["extra"] = extra

        # ログメッセージ整形
        msg = f"[request_id: {extra['request_id']}] {msg}"
        return msg, kwargs

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO)) # 設定ファイルからログレベルを取得

    formatter = SafeFormatter(LOG_FORMATTER)

    # 一度でも setup_logging が呼ばれたら、全ハンドラに SafeFormatter を適用する
    for handler in logger.handlers:
        handler.setFormatter(formatter)

        
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)  # 念のためここでも設定
        logger.addHandler(handler)

def get_logger(request_id=None):
    setup_logging()
    logger = logging.getLogger()
    return RequestLoggerAdapter(logger, {"request_id": request_id}) # 「{"request_id": request_id}」はデフォルトのextra情報