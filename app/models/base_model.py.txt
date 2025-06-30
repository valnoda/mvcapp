import pymysql
import os
from app.core.base_class import BaseClass
import app.config.settings as SETTING

class BaseModel(BaseClass):
    def __init__(self, context=None):
        super().__init__(context)
        self.connection = pymysql.connect(
            host=os.environ[SETTING.DB_HOST],
            user=os.environ[SETTING.DB_USER],
            password=os.environ[SETTING.DB_PASSWORD],
            database=os.environ[SETTING.DB_NAME],
            connect_timeout=5,
            autocommit=False,  # 明示的にcommit()する
            cursorclass=pymysql.cursors.DictCursor  # 結果を辞書形式で取得
        )

    def execute_query(self, query, params=None):
        """SELECT専用"""
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def execute_update(self, query, params=None):
        """INSERT / UPDATE / DELETE 専用"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            raise e

    def run_transaction(self, callback):
        """複数SQLを一括トランザクション処理"""
        try:
            with self.connection.cursor() as cursor:
                result = callback(cursor)
            self.connection.commit()
            return result
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            self.connection.close()

    def close(self):
        self.connection.close()