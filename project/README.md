# University Room & Event Booking System

A complete Room & Event Booking System built with Python Flask and MySQL.

## Features
- **User Authentication**: Student, Faculty, and Admin roles.
- **Room Booking**: View rooms and timeslots, make reservations.
- **Admin Management**: Approve/reject reservations, manage rooms and timeslots.
- **Concurrency Handling**: Prevents double bookings using MySQL transactions.

## Local Setup

1. **Clone the repository** (if applicable) or navigate to the project folder.

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   - Ensure you have MySQL installed and running.
   - Create a database (e.g., `university_booking`).
   - Import the schema and seed data:
     ```bash
     mysql -u root -p university_booking < db/schema.sql
     ```

4. **Environment Variables**:
   - Create a `.env` file in the `project` directory with the following content:
     ```
     SECRET_KEY=your_secret_key
     DB_HOST=localhost
     DB_USER=your_db_user
     DB_PASSWORD=your_db_password
     DB_NAME=university_booking
     ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   - Access the app at `http://localhost:5000`.

## Deployment on Render.com

1. **Create a New Web Service**:
   - Connect your GitHub repository containing this code.

2. **Configure Settings**:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

3. **Environment Variables**:
   - Add the following environment variables in the Render dashboard:
     - `SECRET_KEY`: A strong random string.
     - `DB_HOST`: Your MySQL database host (e.g., from a managed database provider like Aiven or Render's own PostgreSQL if adapted, but this app uses MySQL).
     - `DB_USER`: Database username.
     - `DB_PASSWORD`: Database password.
     - `DB_NAME`: Database name.

4. **Database Connection**:
   - Ensure your MySQL database is accessible from Render (allow public access or VPC peering if supported).

5. **Deploy**:
   - Click "Create Web Service". Render will build and deploy your application.

## Usage

- **Register**: Create a new account.
- **Login**: Log in with your credentials.
- **Book**: Select a room and timeslot to make a reservation.
- **Admin**: Log in as an admin (you may need to manually update a user's role to 'admin' in the database for the first admin) to approve requests and manage resources.
