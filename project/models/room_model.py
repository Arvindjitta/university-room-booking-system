from .db_connection import get_db_connection

class Room:
    @staticmethod
    def get_all_rooms():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        cursor.close()
        conn.close()
        return rooms

    @staticmethod
    def get_room_by_id(room_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
        room = cursor.fetchone()
        cursor.close()
        conn.close()
        return room

    @staticmethod
    def add_room(name, capacity, rtype, location):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rooms (room_name, capacity, room_type, location) VALUES (%s, %s, %s, %s)",
            (name, capacity, rtype, location)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_room(room_id, name, capacity, rtype, location):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE rooms SET room_name=%s, capacity=%s, room_type=%s, location=%s WHERE id=%s",
            (name, capacity, rtype, location, room_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_room(room_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
        conn.commit()
        cursor.close()
        conn.close()

class Timeslot:
    @staticmethod
    def get_all_timeslots():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM timeslots ORDER BY slot_date, start_time")
        slots = cursor.fetchall()
        cursor.close()
        conn.close()
        return slots

    @staticmethod
    def get_timeslot_by_id(slot_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM timeslots WHERE id = %s", (slot_id,))
        slot = cursor.fetchone()
        cursor.close()
        conn.close()
        return slot

    @staticmethod
    def update_timeslot(slot_id, date, start, end):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE timeslots SET slot_date=%s, start_time=%s, end_time=%s WHERE id=%s",
            (date, start, end, slot_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def add_timeslot(date, start, end):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO timeslots (slot_date, start_time, end_time) VALUES (%s, %s, %s)",
            (date, start, end)
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    @staticmethod
    def delete_timeslot(slot_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM timeslots WHERE id = %s", (slot_id,))
        conn.commit()
        cursor.close()
        conn.close()
