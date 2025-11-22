from .db_connection import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def create_user(name, email, password, role='student'):
        conn = get_db_connection()
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                (name, email, password_hash, role)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_user_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    @staticmethod
    def verify_password(stored_hash, password):
        return check_password_hash(stored_hash, password)

    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, role FROM users ORDER BY id")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users

    @staticmethod
    def update_user(user_id, name=None, email=None, password=None, role=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Build dynamic update query based on provided fields
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            if email is not None:
                updates.append("email = %s")
                params.append(email)
            if password is not None:
                updates.append("password_hash = %s")
                params.append(generate_password_hash(password))
            if role is not None:
                updates.append("role = %s")
                params.append(role)
            
            if not updates:
                return False
            
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
