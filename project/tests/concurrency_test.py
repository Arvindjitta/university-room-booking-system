import requests
import threading
import time

# Configuration
BASE_URL = "http://localhost:5001"
LOGIN_URL = f"{BASE_URL}/login"
RESERVE_URL = f"{BASE_URL}/reserve"

# User Credentials (created in previous steps)
USER1 = {"email": "student@test.com", "password": "password"}
USER2 = {"email": "faculty@test.com", "password": "password"}

# Target Booking (Same Room, Same Slot)
# Room 1 (Lecture Hall A), Slot 3 (2023-12-01 11:00-12:00)
ROOM_ID = "2"
SLOT_ID = "3"

def login(session, email, password):
    # Get login page to get CSRF token if needed (Flask-WTF) - but we are using basic HTML forms
    # Just post credentials
    response = session.post(LOGIN_URL, data={"email": email, "password": password})
    if response.url == f"{BASE_URL}/dashboard":
        print(f"Login successful for {email}")
        return True
    else:
        print(f"Login failed for {email}. URL: {response.url}")
        if "Invalid email or password" in response.text:
            print("Reason: Invalid credentials")
        else:
            print(f"Response text snippet: {response.text[:200]}")
        return False

def book_room(user_name, email, password):
    session = requests.Session()
    if not login(session, email, password):
        return

    print(f"{user_name} attempting to book...")
    
    # Simulate simultaneous request
    data = {
        "room_id": ROOM_ID,
        "slot_id": SLOT_ID,
        "purpose": f"Concurrency Test by {user_name}"
    }
    
    start_time = time.time()
    response = session.post(RESERVE_URL, data=data)
    end_time = time.time()
    
    # Check for success message or error
    if "Reservation request submitted successfully" in response.text:
        print(f"SUCCESS: {user_name} booked the room! (Time: {end_time - start_time:.4f}s)")
    elif "Room is already booked" in response.text:
        print(f"BLOCKED: {user_name} was prevented from double booking. (Time: {end_time - start_time:.4f}s)")
    else:
        print(f"UNKNOWN: {user_name} got unexpected response.")
        print(f"Response snippet: {response.text[:500]}")

# Create threads
t1 = threading.Thread(target=book_room, args=("Student", USER1["email"], USER1["password"]))
t2 = threading.Thread(target=book_room, args=("Faculty", USER2["email"], USER2["password"]))

print("Starting Concurrency Test...")
# Start threads simultaneously
t1.start()
t2.start()

t1.join()
t2.join()
print("Test Complete.")
