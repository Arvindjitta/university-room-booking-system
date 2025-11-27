from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.room_model import Room, Timeslot
from models.reservation_model import Reservation

reservation_bp = Blueprint('reservation', __name__)

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@reservation_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user_role = session.get('role')
    
    # Admin Dashboard
    if user_role == 'admin':
        from models.user_model import User
        
        # Get all reservations
        all_reservations = Reservation.get_all_reservations()
        
        # Count reservations by status
        pending_approvals = sum(1 for r in all_reservations if r['status'] == 'pending')
        approved_count = sum(1 for r in all_reservations if r['status'] == 'approved')
        rejected_count = sum(1 for r in all_reservations if r['status'] == 'rejected')
        
        # Get total counts
        all_users = User.get_all_users()
        total_users = len(all_users)
        
        all_rooms = Room.get_all_rooms()
        total_rooms = len(all_rooms)
        
        all_timeslots = Timeslot.get_all_timeslots()
        total_timeslots = len(all_timeslots)
        
        # Get recent reservations (last 5)
        recent_reservations = all_reservations[:5]
        
        return render_template('dashboard.html',
                             is_admin=True,
                             pending_approvals=pending_approvals,
                             approved_count=approved_count,
                             rejected_count=rejected_count,
                             total_users=total_users,
                             total_rooms=total_rooms,
                             total_timeslots=total_timeslots,
                             recent_reservations=recent_reservations)
    
    # Student/Faculty Dashboard
    else:
        # Get user's reservations
        user_reservations = Reservation.get_reservations_by_user(user_id)
        
        # Count pending and approved reservations for this user
        pending_count = sum(1 for r in user_reservations if r['status'] == 'pending')
        approved_count = sum(1 for r in user_reservations if r['status'] == 'approved')
        
        # Get all rooms
        all_rooms = Room.get_all_rooms()
        
        # Filter rooms for students (capacity <= 10)
        if user_role == 'student':
            available_rooms = [r for r in all_rooms if r['capacity'] <= 10]
        else:
            available_rooms = all_rooms
        
        available_rooms_count = len(available_rooms)
        
        # Get sample rooms for preview (first 3)
        sample_rooms = available_rooms[:3] if len(available_rooms) >= 3 else available_rooms
        
        return render_template('dashboard.html',
                             is_admin=False,
                             pending_count=pending_count,
                             approved_count=approved_count,
                             available_rooms_count=available_rooms_count,
                             sample_rooms=sample_rooms)

@reservation_bp.route('/rooms')
@login_required
def rooms():
    all_rooms = Room.get_all_rooms()
    return render_template('rooms.html', rooms=all_rooms)

@reservation_bp.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    if request.method == 'POST':
        room_id = request.form['room_id']
        slot_id = request.form['slot_id']
        purpose = request.form['purpose']
        user_id = session['user_id']
        
        room = Room.get_room_by_id(room_id)
        if session.get('role') == 'student' and room['capacity'] > 10:
            flash('Students cannot book rooms with capacity greater than 10.', 'danger')
            return redirect(url_for('reservation.reserve'))

        success, message = Reservation.create_reservation(user_id, room_id, slot_id, purpose)
        if success:
            flash(message, 'success')
            return redirect(url_for('reservation.my_reservations'))
        else:
            flash(message, 'danger')
            
    all_rooms = Room.get_all_rooms()
    # Filter rooms for students in the dropdown
    if session.get('role') == 'student':
        all_rooms = [r for r in all_rooms if r['capacity'] <= 10]
        
    all_slots = Timeslot.get_all_timeslots()
    return render_template('reserve.html', rooms=all_rooms, slots=all_slots)

@reservation_bp.route('/my_reservations')
@login_required
def my_reservations():
    user_id = session['user_id']
    reservations = Reservation.get_reservations_by_user(user_id)
    return render_template('my_reservations.html', reservations=reservations)
