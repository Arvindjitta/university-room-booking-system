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
    return render_template('dashboard.html')

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
