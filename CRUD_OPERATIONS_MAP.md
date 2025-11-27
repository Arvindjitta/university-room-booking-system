# CRUD Operations Map - University Room & Event Booking System

This document maps all **Create, Read, Update, Delete (CRUD)** operations in the project.

---

## 📊 Summary Table

| Entity | Create | Read | Update | Delete | Location |
|--------|--------|------|--------|--------|----------|
| **Users** | ✅ | ✅ | ✅ | ✅ | `models/user_model.py` |
| **Rooms** | ✅ | ✅ | ✅ | ✅ | `models/room_model.py` |
| **Timeslots** | ✅ | ✅ | ✅ | ✅ | `models/room_model.py` |
| **Reservations** | ✅ | ✅ | ✅ | ✅ | `models/reservation_model.py` |
| **Approvals** | ✅ | ✅ | ❌ | ✅ | `models/reservation_model.py` |

---

## 1️⃣ USERS - Full CRUD

### 📁 File: `project/models/user_model.py`

### ✅ CREATE
```python
User.create_user(name, email, password, role='student')
```
**SQL:** `INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)`

**Used by:**
- `routes/auth_routes.py` → `/register` (User self-registration)
- `routes/admin_routes.py` → `/admin/users/create` (Admin creates user)

---

### 📖 READ
**Method 1: Get Single User by Email**
```python
User.get_user_by_email(email)
```
**SQL:** `SELECT * FROM users WHERE email = %s`

**Used by:**
- `routes/auth_routes.py` → `/login` (Authentication)

**Method 2: Get Single User by ID**
```python
User.get_user_by_id(user_id)
```
**SQL:** `SELECT * FROM users WHERE id = %s`

**Used by:**
- `routes/admin_routes.py` → `/admin/users/<id>/edit` (Load user for editing)

**Method 3: Get All Users**
```python
User.get_all_users()
```
**SQL:** `SELECT id, name, email, role FROM users ORDER BY id`

**Used by:**
- `routes/admin_routes.py` → `/admin/users` (List all users)

---

### 🔄 UPDATE
```python
User.update_user(user_id, name=None, email=None, password=None, role=None)
```
**SQL:** Dynamic `UPDATE users SET [fields] WHERE id = %s`

**Used by:**
- `routes/admin_routes.py` → `/admin/users/<id>/edit` (Admin updates user)

---

### ❌ DELETE
```python
User.delete_user(user_id)
```
**SQL:** `DELETE FROM users WHERE id = %s`

**Used by:**
- `routes/admin_routes.py` → `/admin/users/<id>/delete` (Admin deletes user)

---

## 2️⃣ ROOMS - Full CRUD

### 📁 File: `project/models/room_model.py`

### ✅ CREATE
```python
Room.add_room(name, capacity, rtype, location)
```
**SQL:** `INSERT INTO rooms (room_name, capacity, room_type, location) VALUES (%s, %s, %s, %s)`

**Used by:**
- `routes/admin_routes.py` → `/admin/rooms` (Admin adds room)

---

### 📖 READ
**Method 1: Get All Rooms**
```python
Room.get_all_rooms()
```
**SQL:** `SELECT * FROM rooms`

**Used by:**
- `routes/admin_routes.py` → `/admin/rooms` (Admin views all rooms)
- `routes/reservation_routes.py` → `/rooms` (Students/Faculty view rooms)
- `routes/reservation_routes.py` → `/reserve` (Booking form)

**Method 2: Get Single Room by ID**
```python
Room.get_room_by_id(room_id)
```
**SQL:** `SELECT * FROM rooms WHERE id = %s`

**Used by:**
- `routes/admin_routes.py` → `/admin/rooms/<id>/edit` (Load room for editing)

---

### 🔄 UPDATE
```python
Room.update_room(room_id, name, capacity, rtype, location)
```
**SQL:** `UPDATE rooms SET room_name=%s, capacity=%s, room_type=%s, location=%s WHERE id=%s`

**Used by:**
- `routes/admin_routes.py` → `/admin/rooms/<id>/edit` (Admin updates room)

---

### ❌ DELETE
```python
Room.delete_room(room_id)
```
**SQL:** `DELETE FROM rooms WHERE id = %s`

**Used by:**
- `routes/admin_routes.py` → `/admin/rooms` (Admin deletes room)

---

## 3️⃣ TIMESLOTS - Full CRUD

### 📁 File: `project/models/room_model.py` (Timeslot class)

### ✅ CREATE
```python
Timeslot.add_timeslot(date, start, end)
```
**SQL:** `INSERT INTO timeslots (slot_date, start_time, end_time) VALUES (%s, %s, %s)`

**Used by:**
- `routes/admin_routes.py` → `/admin/timeslots` (Admin adds timeslot)

---

### 📖 READ
**Method 1: Get All Timeslots**
```python
Timeslot.get_all_timeslots()
```
**SQL:** `SELECT * FROM timeslots ORDER BY slot_date, start_time`

**Used by:**
- `routes/admin_routes.py` → `/admin/timeslots` (Admin views all timeslots)
- `routes/reservation_routes.py` → `/reserve` (Students/Faculty view available slots)

**Method 2: Get Single Timeslot by ID**
```python
Timeslot.get_timeslot_by_id(slot_id)
```
**SQL:** `SELECT * FROM timeslots WHERE id = %s`

**Used by:**
- `routes/admin_routes.py` → `/admin/timeslots/<id>/edit` (Load timeslot for editing)

---

### 🔄 UPDATE
```python
Timeslot.update_timeslot(slot_id, date, start, end)
```
**SQL:** `UPDATE timeslots SET slot_date=%s, start_time=%s, end_time=%s WHERE id=%s`

**Used by:**
- `routes/admin_routes.py` → `/admin/timeslots/<id>/edit` (Admin updates timeslot)

---

### ❌ DELETE
```python
Timeslot.delete_timeslot(slot_id)
```
**SQL:** `DELETE FROM timeslots WHERE id = %s`

**Used by:**
- `routes/admin_routes.py` → `/admin/timeslots` (Admin deletes timeslot)

---

## 4️⃣ RESERVATIONS - Full CRUD (with special operations)

### 📁 File: `project/models/reservation_model.py`

### ✅ CREATE
```python
Reservation.create_reservation(user_id, room_id, slot_id, purpose)
```
**SQL:** 
```sql
-- Check for conflicts (with row lock)
SELECT id FROM reservations 
WHERE room_id = %s AND slot_id = %s AND status IN ('approved', 'pending')
FOR UPDATE

-- Insert if no conflict
INSERT INTO reservations (user_id, room_id, slot_id, purpose, status)
VALUES (%s, %s, %s, %s, 'pending')
```
**Features:** Transaction-based, prevents double booking

**Used by:**
- `routes/reservation_routes.py` → `/reserve` (Students/Faculty create reservation)

---

### 📖 READ
**Method 1: Get Reservations by User**
```python
Reservation.get_reservations_by_user(user_id)
```
**SQL:**
```sql
SELECT r.*, rm.room_name, t.slot_date, t.start_time, t.end_time 
FROM reservations r
JOIN rooms rm ON r.room_id = rm.id
JOIN timeslots t ON r.slot_id = t.id
WHERE r.user_id = %s
ORDER BY r.created_at DESC
```

**Used by:**
- `routes/reservation_routes.py` → `/my-reservations` (User views their own reservations)

**Method 2: Get All Reservations**
```python
Reservation.get_all_reservations()
```
**SQL:**
```sql
SELECT r.*, u.name as user_name, rm.room_name, t.slot_date, t.start_time, t.end_time 
FROM reservations r
JOIN users u ON r.user_id = u.id
JOIN rooms rm ON r.room_id = rm.id
JOIN timeslots t ON r.slot_id = t.id
ORDER BY r.created_at DESC
```

**Used by:**
- `routes/admin_routes.py` → `/admin/approvals` (Admin views all reservations)

---

### 🔄 UPDATE
```python
Reservation.update_status(reservation_id, status, admin_id, notes="")
```
**SQL:**
```sql
-- Update reservation status
UPDATE reservations SET status = %s WHERE id = %s

-- Insert approval record
INSERT INTO approvals (reservation_id, admin_id, decision, notes)
VALUES (%s, %s, %s, %s)
```
**Features:** Transaction-based, creates approval record

**Used by:**
- `routes/admin_routes.py` → `/admin/approve/<id>` (Admin approves/rejects reservation)

---

### ❌ DELETE
**Method 1: Delete by Status**
```python
Reservation.clear_by_status(status)
```
**SQL:** `DELETE FROM reservations WHERE status = %s`

**Used by:**
- `routes/admin_routes.py` → `/admin/clear_reservations` (Admin clears cancelled/rejected)

**Method 2: Delete All (Dangerous)**
```python
Reservation.clear_all_reservations()
```
**SQL:**
```sql
SET FOREIGN_KEY_CHECKS = 0
TRUNCATE TABLE approvals
TRUNCATE TABLE reservations
SET FOREIGN_KEY_CHECKS = 1
```

**Used by:**
- `routes/admin_routes.py` → `/admin/clear_reservations` (Admin clears all reservations)

**⚠️ Note:** No individual reservation delete - users can only change status to 'cancelled'

---

## 5️⃣ APPROVALS - Limited CRUD

### 📁 File: `project/models/reservation_model.py` (part of Reservation class)

### ✅ CREATE
Created automatically when `Reservation.update_status()` is called
```sql
INSERT INTO approvals (reservation_id, admin_id, decision, notes)
VALUES (%s, %s, %s, %s)
```

---

### 📖 READ
Currently read via JOIN queries in `Reservation.get_all_reservations()`

---

### 🔄 UPDATE
❌ No update operation - approvals are immutable audit records

---

### ❌ DELETE
Deleted automatically when `Reservation.clear_all_reservations()` is called

---

## 📍 Route-to-Model Mapping

### Admin Routes (`routes/admin_routes.py`)
| Route | Method | Model Operation | CRUD Type |
|-------|--------|-----------------|-----------|
| `/admin/users` | GET | `User.get_all_users()` | Read |
| `/admin/users/create` | POST | `User.create_user()` | Create |
| `/admin/users/<id>/edit` | GET | `User.get_user_by_id()` | Read |
| `/admin/users/<id>/edit` | POST | `User.update_user()` | Update |
| `/admin/users/<id>/delete` | POST | `User.delete_user()` | Delete |
| `/admin/rooms` | GET | `Room.get_all_rooms()` | Read |
| `/admin/rooms` | POST (add) | `Room.add_room()` | Create |
| `/admin/rooms/<id>/edit` | GET | `Room.get_room_by_id()` | Read |
| `/admin/rooms/<id>/edit` | POST | `Room.update_room()` | Update |
| `/admin/rooms` | POST (delete) | `Room.delete_room()` | Delete |
| `/admin/timeslots` | GET | `Timeslot.get_all_timeslots()` | Read |
| `/admin/timeslots` | POST (add) | `Timeslot.add_timeslot()` | Create |
| `/admin/timeslots/<id>/edit` | GET | `Timeslot.get_timeslot_by_id()` | Read |
| `/admin/timeslots/<id>/edit` | POST | `Timeslot.update_timeslot()` | Update |
| `/admin/timeslots` | POST (delete) | `Timeslot.delete_timeslot()` | Delete |
| `/admin/approvals` | GET | `Reservation.get_all_reservations()` | Read |
| `/admin/approve/<id>` | POST | `Reservation.update_status()` | Update |
| `/admin/clear_reservations` | POST | `Reservation.clear_by_status()` or `.clear_all_reservations()` | Delete |

### User Routes (`routes/reservation_routes.py`)
| Route | Method | Model Operation | CRUD Type |
|-------|--------|-----------------|-----------|
| `/rooms` | GET | `Room.get_all_rooms()` | Read |
| `/reserve` | GET | `Room.get_all_rooms()`, `Timeslot.get_all_timeslots()` | Read |
| `/reserve` | POST | `Reservation.create_reservation()` | Create |
| `/my-reservations` | GET | `Reservation.get_reservations_by_user()` | Read |

### Auth Routes (`routes/auth_routes.py`)
| Route | Method | Model Operation | CRUD Type |
|-------|--------|-----------------|-----------|
| `/login` | POST | `User.get_user_by_email()` | Read |
| `/register` | POST | `User.create_user()` | Create |

---

## 📈 CRUD Coverage Summary

✅ **Users**: 100% CRUD (Create, Read, Update, Delete)  
✅ **Rooms**: 100% CRUD (Create, Read, Update, Delete)  
✅ **Timeslots**: 100% CRUD (Create, Read, Update, Delete)  
✅ **Reservations**: 100% CRUD (Create, Read, Update, Delete*)  
⚠️ **Approvals**: 50% CRUD (Create, Read only - immutable by design)

*Note: Reservations don't have individual delete - only bulk delete by status

---

## 🎯 Key Takeaways

1. **All primary entities have full CRUD operations**
2. **Approvals are audit records** (immutable, created with approvals)
3. **No ORM used** - all operations use raw SQL
4. **Transaction support** for critical operations (reservations, approvals)
5. **Concurrency control** via `SELECT ... FOR UPDATE` in reservations
6. **Soft delete pattern** for reservations (status = 'cancelled' instead of DELETE)
