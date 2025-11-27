# University Room & Event Booking System - Project Documentation

## 1. Database Purpose

### Why is the database needed?
The database is the central component of the University Room & Event Booking System that stores and manages all persistent data. Without it, the system would lose all information when the application restarts. The database ensures:

- **Data Persistence**: Stores room details, user accounts, timeslots, and reservations permanently
- **Data Integrity**: Maintains relationships between entities (e.g., which user booked which room)
- **Concurrent Access**: Allows multiple users to interact with the system simultaneously without conflicts
- **Security**: Stores sensitive information like password hashes securely
- **Audit Trail**: Tracks reservation approvals and maintains history through the approvals table

### What should the database do?

The database should provide the following core functionalities:

1. **User Management**
   - Store user credentials (name, email, hashed passwords)
   - Differentiate between user roles (student, faculty, admin)
   - Support authentication and authorization

2. **Room Management**
   - Maintain inventory of available rooms
   - Store room properties (capacity, type, location)
   - Enable searching and filtering of rooms

3. **Timeslot Management**
   - Define available booking time periods
   - Track date and time ranges for bookings
   - Support recurring and one-time slots

4. **Reservation Management**
   - Link users to rooms and timeslots
   - Track reservation status (pending, approved, rejected, cancelled)
   - Handle concurrent booking requests
   - Prevent double bookings through constraints

5. **Approval Workflow**
   - Record admin decisions on reservations
   - Store approval/rejection notes
   - Maintain audit trail with timestamps

---

## 2. Users and Their Information Needs

### User Types and Access Levels

#### **Students** (Role: `student`)
**Information Needs:**
- View available rooms and their details
- See available timeslots
- View their own reservation history
- Check reservation status (pending/approved/rejected)

**Functions:**
- Browse rooms by capacity, type, location
- Create new room reservations
- Cancel their own pending reservations
- Receive notifications about approval/rejection

#### **Faculty** (Role: `faculty`)
**Information Needs:**
- Same as students
- Priority booking capabilities (handled by admin approval workflow)

**Functions:**
- All student functions
- May have faster approval times (business logic in admin review)
- Can book larger rooms or specialized spaces

#### **Administrators** (Role: `admin`)
**Information Needs:**
- View ALL reservations across all users
- Access user management data
- Monitor room utilization
- Track approval history

**Functions:**
- **Approve/Reject** reservation requests
- **Manage Rooms**: Create, edit, delete rooms
- **Manage Timeslots**: Create, edit, delete timeslots
- **Manage Users**: Create, edit, delete user accounts
- **Clear Reservations**: Bulk delete cancelled/rejected entries
- **Generate Reports**: View system-wide statistics

---

## 3. Input Data and Storage Requirements

### Input Data Available to the Database

#### **During System Setup:**
- Initial room inventory (from schema.sql seed data)
- Default timeslots (from schema.sql seed data)
- Admin user account

#### **From User Registration:**
- Name
- Email address
- Password (stored as bcrypt hash)
- Role assignment (student/faculty/admin)

#### **From Room Creation (Admin):**
- Room name
- Capacity (integer)
- Room type (Lab, Lecture Hall, Conference Room, etc.)
- Location (building/floor information)

#### **From Timeslot Creation (Admin):**
- Date (YYYY-MM-DD)
- Start time (HH:MM:SS)
- End time (HH:MM:SS)

#### **From Reservation Requests (Students/Faculty):**
- Room ID
- Timeslot ID
- User ID (from session)
- Timestamp of request

#### **From Approval Actions (Admin):**
- Reservation ID
- Approval decision (approve/reject)
- Admin notes/comments
- Admin user ID

### Information Stored in the Database

The database stores structured data across 5 main tables:

1. **users**: Authentication and role information
2. **rooms**: Physical space inventory
3. **timeslots**: Available booking periods
4. **reservations**: Booking records with status
5. **approvals**: Admin decision history

---

## 4. Entity-Relationship (ER) Diagram

```
┌─────────────────────┐
│       USERS         │
├─────────────────────┤
│ PK: id              │
│     name            │
│     email (UNIQUE)  │
│     password_hash   │
│     role            │
└──────────┬──────────┘
           │
           │ creates
           │ (1:N)
           ▼
┌─────────────────────┐
│    RESERVATIONS     │
├─────────────────────┤
│ PK: id              │
│ FK: user_id         │────┐
│ FK: room_id         │────┼──┐
│ FK: timeslot_id     │────┼──┼──┐
│     status          │    │  │  │
│     created_at      │    │  │  │
└─────────────────────┘    │  │  │
           │               │  │  │
           │ receives      │  │  │
           │ (1:1)         │  │  │
           ▼               │  │  │
┌─────────────────────┐    │  │  │
│     APPROVALS       │    │  │  │
├─────────────────────┤    │  │  │
│ PK: id              │    │  │  │
│ FK: reservation_id  │    │  │  │
│ FK: admin_id        │────┘  │  │
│     decision        │        │  │
│     notes           │        │  │
│     approved_at     │        │  │
└─────────────────────┘        │  │
                               │  │
                               │  │
                    for        │  │
                    (N:1)      │  │
┌─────────────────────┐        │  │
│       ROOMS         │◄───────┘  │
├─────────────────────┤           │
│ PK: id              │           │
│     room_name       │           │
│     capacity        │           │
│     room_type       │           │
│     location        │           │
└─────────────────────┘           │
                                  │
                       during     │
                       (N:1)      │
┌─────────────────────┐           │
│     TIMESLOTS       │◄──────────┘
├─────────────────────┤
│ PK: id              │
│     slot_date       │
│     start_time      │
│     end_time        │
└─────────────────────┘
```

### Relationships Explained:

1. **USERS → RESERVATIONS** (1:N)
   - One user can create many reservations
   - Each reservation belongs to one user

2. **ROOMS → RESERVATIONS** (1:N)
   - One room can be reserved multiple times
   - Each reservation is for one room

3. **TIMESLOTS → RESERVATIONS** (1:N)
   - One timeslot can be booked for different rooms
   - Each reservation uses one timeslot

4. **RESERVATIONS → APPROVALS** (1:1)
   - Each reservation has at most one approval record
   - Each approval belongs to one reservation

5. **USERS (admin) → APPROVALS** (1:N)
   - One admin can approve many reservations
   - Each approval is made by one admin

### Key Constraints:

- **UNIQUE(room_id, timeslot_id)** in reservations: Prevents double booking
- **Foreign Keys**: Maintain referential integrity
- **NOT NULL**: Ensures required fields are always populated
- **ENUM for status**: Limits reservation status to valid values

---

## 5. Team Roles and Responsibilities (5 Members)

### **Member 1: Project Lead & Database Designer**
**Responsibilities:**
- Design and implement database schema (schema.sql)
- Create ER diagram and normalize tables
- Define relationships and constraints
- Write database initialization scripts
- Oversee project timeline and deliverables
- Coordinate between team members
- Handle Railway deployment configuration

**Deliverables:**
- `project/db/schema.sql`
- ER diagram documentation
- Database normalization report
- Deployment guide

---

### **Member 2: Backend Developer - User Management**
**Responsibilities:**
- Implement User model (`user_model.py`)
- Create authentication routes (`auth_routes.py`)
- Develop user CRUD operations
- Implement password hashing and security
- Create user management UI for admins
- Write unit tests for user functionality

**Deliverables:**
- `project/models/user_model.py`
- `project/routes/auth_routes.py`
- User-related admin routes
- Authentication templates (login, register)
- User management templates

---

### **Member 3: Backend Developer - Reservation System**
**Responsibilities:**
- Implement Reservation model (`reservation_model.py`)
- Create reservation routes (`reservation_routes.py`)
- Develop concurrency control mechanisms
- Implement approval workflow
- Handle status transitions (pending → approved/rejected)
- Write integration tests for booking flow

**Deliverables:**
- `project/models/reservation_model.py`
- `project/routes/reservation_routes.py`
- Reservation templates (book room, my reservations)
- Concurrency testing report

---

### **Member 4: Backend Developer - Room & Timeslot Management**
**Responsibilities:**
- Implement Room and Timeslot models (`room_model.py`)
- Create admin routes for room/timeslot CRUD
- Develop search and filtering functionality
- Implement admin dashboard features
- Create timeslot scheduling logic
- Write API documentation

**Deliverables:**
- `project/models/room_model.py`
- Admin management routes
- Room and timeslot templates
- API endpoint documentation

---

### **Member 5: Frontend Developer & UI/UX Designer**
**Responsibilities:**
- Design and implement all HTML templates
- Create responsive layouts using Bootstrap
- Implement navigation and user flows
- Design role-based UI elements (student/faculty/admin views)
- Ensure accessibility and usability
- Create project demo video
- Write user documentation

**Deliverables:**
- `project/templates/layout.html`
- All page templates (dashboard, booking forms, admin panels)
- CSS styling and UI components
- User manual and screenshots
- Demo video/presentation

---

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **ORM/Query**: mysql-connector-python (raw SQL)
- **Authentication**: Flask sessions + Werkzeug password hashing
- **Frontend**: HTML, Bootstrap 5, Jinja2 templates
- **Deployment**: Railway.app
- **Version Control**: Git/GitHub

---

## Project Timeline (Example)

| Week | Milestone |
|------|-----------|
| 1    | Requirements gathering, ER diagram design, schema creation |
| 2    | Database setup, user authentication, basic models |
| 3    | Room and timeslot management, admin panel |
| 4    | Reservation system, approval workflow |
| 5    | Frontend templates, UI/UX refinement |
| 6    | Testing, bug fixes, deployment to Railway |
| 7    | Documentation, demo video, final presentation |

---

## Conclusion

This University Room & Event Booking System demonstrates a complete full-stack application with proper separation of concerns, role-based access control, and a well-structured relational database. The division of work ensures each team member has clear responsibilities while maintaining integration points for collaboration.
