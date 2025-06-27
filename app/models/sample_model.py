from app.models.base_model import BaseModel

class SampleModel(BaseModel):
    def get_all_users(self):
        query = "SELECT * FROM users"
        return self.execute_query(query)

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = %s"
        return self.execute_query(query, (user_id,))

    def add_user(self, name, email, amount):
        query = "INSERT INTO users (name, email, amount) VALUES (%s, %s, %s)"
        return self.execute_update(query, (name, email, amount))

    def update_user_email(self, user_id, email):
        query = "UPDATE users SET email = %s WHERE id = %s"
        return self.execute_update(query, (email, user_id))

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id = %s"
        return self.execute_update(query, (user_id,))

    def transfer_balance(self, from_id, to_id, amount):
        """残高をユーザー間で送金（トランザクション）"""
        def callback(cursor):
            cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, from_id))
            cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, to_id))
            return True

        return self.run_transaction(callback)