from .db_connection import get_db_connection

class Reservation:
    @staticmethod
    def create_reservation(user_id, room_id, slot_id, purpose):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Start transaction
            conn.start_transaction()
            
            # Check for existing approved or pending reservation for same room and slot
            # Use SELECT ... FOR UPDATE to lock rows
            query = """
                SELECT id FROM reservations 
                WHERE room_id = %s AND slot_id = %s AND status IN ('approved', 'pending')
                FOR UPDATE
            """
            cursor.execute(query, (room_id, slot_id))
            existing = cursor.fetchone()
            
            if existing:
                conn.rollback()
                return False, "Room is already booked or pending approval for this timeslot."
            
            # Insert new reservation
            insert_query = """
                INSERT INTO reservations (user_id, room_id, slot_id, purpose, status)
                VALUES (%s, %s, %s, %s, 'pending')
            """
            cursor.execute(insert_query, (user_id, room_id, slot_id, purpose))
            conn.commit()
            return True, "Reservation request submitted successfully."
            
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_reservations_by_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT r.*, rm.room_name, t.slot_date, t.start_time, t.end_time 
            FROM reservations r
            JOIN rooms rm ON r.room_id = rm.id
            JOIN timeslots t ON r.slot_id = t.id
            WHERE r.user_id = %s
            ORDER BY r.created_at DESC
        """
        cursor.execute(query, (user_id,))
        reservations = cursor.fetchall()
        cursor.close()
        conn.close()
        return reservations

    @staticmethod
    def get_all_reservations():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT r.*, u.name as user_name, rm.room_name, t.slot_date, t.start_time, t.end_time 
            FROM reservations r
            JOIN users u ON r.user_id = u.id
            JOIN rooms rm ON r.room_id = rm.id
            JOIN timeslots t ON r.slot_id = t.id
            ORDER BY r.created_at DESC
        """
        cursor.execute(query)
        reservations = cursor.fetchall()
        cursor.close()
        conn.close()
        return reservations

    @staticmethod
    def update_status(reservation_id, status, admin_id, notes=""):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            
            update_query = "UPDATE reservations SET status = %s WHERE id = %s"
            cursor.execute(update_query, (status, reservation_id))
            
            approval_query = """
                INSERT INTO approvals (reservation_id, admin_id, decision, notes)
                VALUES (%s, %s, %s, %s)
            """
            # Map status to decision
            decision = 'approved' if status == 'approved' else 'rejected'
            cursor.execute(approval_query, (reservation_id, admin_id, decision, notes))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error updating reservation status: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def clear_by_status(status):
        """Clear reservations with a specific status (cancelled or rejected)"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM reservations WHERE status = %s", (status,))
            connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()
            return affected_rows
        except Exception as e:
            print(f"Error clearing reservations by status: {e}")
            return 0

    @staticmethod
    def clear_all_reservations():
        """Clear all reservations (admin only, dangerous operation)"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            # First clear approvals to avoid FK constraint
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE approvals")
            cursor.execute("TRUNCATE TABLE reservations")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"Error clearing all reservations: {e}")
            return False

