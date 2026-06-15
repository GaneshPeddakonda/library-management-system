# models/member.py
from utils.db_connection import execute_query

class Member:
    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM members ORDER BY full_name")

    @staticmethod
    def get_by_id(member_id):
        rows = execute_query("SELECT * FROM members WHERE id=%s", (member_id,))
        return rows[0] if rows else None

    @staticmethod
    def create(full_name, email, phone, address):
        return execute_query(
            "INSERT INTO members (full_name,email,phone,address) VALUES (%s,%s,%s,%s)",
            (full_name, email, phone, address),
            fetch=False
        )

    @staticmethod
    def update(member_id, **fields):
        set_clause = ", ".join(f"{k}=%s" for k in fields)
        values = list(fields.values()) + [member_id]
        return execute_query(f"UPDATE members SET {set_clause} WHERE id=%s", values, fetch=False)

    @staticmethod
    def delete(member_id):
        return execute_query("DELETE FROM members WHERE id=%s", (member_id,), fetch=False)
