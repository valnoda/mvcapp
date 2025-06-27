from app.controllers.base_controller import BaseController
from app.utils.validator import validate_input
import app.config.constants as CONST
from urllib.parse import parse_qs
from app.models.sample_model import SampleModel
from app.utils.common import to_json
import re

class SampleController(BaseController):
    def __init__(self, context=None):
        super().__init__(context)

    def handle(self, event):
        # super().__init__() # 親クラスのコンストラクタを実行 ※今回の場合はSampleControllerで__init__を定義していない（オーバーライドされていない）ため不要ですが念のため追加
        self.logger.info("### SampleController.handle() 開始 ###", extra={"user_id": 123})  # ← ここで利用（logger.pyでフォーマットに%(user_id)sを追加している）

        # 返却値初期化
        res = {}

        body = event.get("body", "")
        form_data = parse_qs(body)
        key1 = form_data.get("key1", [""])[0]
        key2 = form_data.get("key2", [""])[0]

        validate_input(key1, key2)
        joined = f"{key1}{CONST.SEPARATOR}{key2}"

        # 最初の３文字を取得
        match = re.fullmatch(r'([a-zA-Z]{3})(\d+)', key1)
        if match:
            prefix = match.group(1)  # 最初の3文字
            number = int(match.group(2))  # その後の数値をintに変換

        else:
            return {"re_val1":joined, "res":false}

        # DBアクセス
        model = SampleModel(self.context)

        # 全権取得
        if prefix == 'all':
            res = model.get_all_users()
            print('### get_all_users ###', res)

        # 取得
        if prefix == 'get':
            res = model.get_user_by_id(number)
            print('### get_user_by_id ###', res)
        
        # アップデート
        if prefix == 'upd':
            res = model.update_user_email(number, f'test@test.com{number}')
            print('### update_user_email ###', res)

        # 追加
        if prefix == 'ins':
            res = model.add_user(f'testname{number}', f'testini@test.com{number}', int(f"{123}{number}"))
            print('### add_user ###', res)

        # 削除
        if prefix == 'del':
            res = model.delete_user(number)
            print('### delete_user ###', res)

        return {"re_val1":joined, "res":res}

