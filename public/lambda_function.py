from app.utils.logger import get_logger
from app.controllers.sample_controller import SampleController
from app.exceptions.custom_exceptions import ValidationError
from app.utils.common import to_json
import copy

import os

def lambda_handler(event, context):
    try:


        print("========= 環境変数チェック =========")
        print("DB_HOST:", os.environ.get("DB_HOST"))
        print("DB_USER:", os.environ.get("DB_USER"))
        print("===================================")

        controller = SampleController(context)

        # ログ：リクエスト（マスク処理を挟んでもよい）
        controller.logger.info(f"Incoming event: {to_json(sanitize_event(event))}")

        # 例外発生テスト
        # raise Exception("例外発生")
        # raise ValidationError("無効なデータです", errors={"field": "必須です"})

        # controller.handleを実行
        response_data = controller.handle(event)

        # ログ：レスポンス
        controller.logger.info(f"Response: {to_json(response_data)}")
        return controller.build_response(
            status=0,
            message="",
            data=response_data,
            errors={},
            status_code=200
        )

    except ValidationError as ve: # バリデーションエラー
        return controller.build_response(
            status=1,
            message=ve.message,
            data={},
            errors=ve.errors,
            status_code=400
        )

    except Exception as e:
        # fallback: controller が存在しないケースへの保険
        logger = get_logger(request_id=getattr(context, "aws_request_id", "-"))
        logger.exception("Unexpected error during controller init or handling")

        # controller が存在していれば build_response() を使う
        if 'controller' in locals():
            return controller.build_response(
                status=1,
                message="内部エラーが発生しました",
                data={},
                errors={},
                status_code=500
            )
        else:
            return {
                "statusCode": 500,
                "body": to_json({
                    "status": 1,
                    "message": "内部エラーが発生しました",
                    "data": {},
                    "errors": {},
                })
            }

def sanitize_event(event):
    event_copy = copy.deepcopy(event)

    if "headers" in event_copy:
        event_copy["headers"] = {
            key: ("***" if key.lower() == "authorization" else value)
            for key, value in event_copy["headers"].items()
        }

    return event_copy