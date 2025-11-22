from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.room_model import Room, Timeslot
from models.reservation_model import Reservation
from models.user_model import User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('reservation.dashboard'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin_bp.route('/approvals')
@admin_required
def approvals():
    reservations = Reservation.get_all_reservations()
    return render_template('admin_approvals.html', reservations=reservations)

@admin_bp.route('/approve/<int:res_id>', methods=['POST'])
@admin_required
def approve_reservation(res_id):
    action = request.form['action'] # 'approve' or 'reject'
    notes = request.form.get('notes', '')
    admin_id = session['user_id']
    
    status = 'approved' if action == 'approve' else 'rejected'
    
    if Reservation.update_status(res_id, status, admin_id, notes):
        flash(f'Reservation {status}.', 'success')
    else:
        flash('Error updating reservation.', 'danger')
        
    return redirect(url_for('admin.approvals'))

@admin_bp.route('/clear_reservations', methods=['GET', 'POST'])
@admin_required
def clear_reservations():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'clear_cancelled':
            count = Reservation.clear_by_status('cancelled')
            flash(f'{count} cancelled reservations cleared successfully!', 'success')
        
        elif action == 'clear_rejected':
            count = Reservation.clear_by_status('rejected')
            flash(f'{count} rejected reservations cleared successfully!', 'success')
        
        elif action == 'clear_all':
            if Reservation.clear_all_reservations():
                flash('All reservations cleared successfully!', 'success')
            else:
                flash('Error clearing reservations.', 'danger')
        
        return redirect(url_for('admin.clear_reservations'))
    
    return render_template('admin_clear_reservations.html')

@admin_bp.route('/rooms', methods=['GET', 'POST'])
@admin_required
def manage_rooms():
    if request.method == 'POST':
        if 'delete' in request.form:
            Room.delete_room(request.form['room_id'])
            flash('Room deleted.', 'success')
        elif 'edit' in request.form:
            # redirect to edit page
            return redirect(url_for('admin.edit_room', room_id=request.form['room_id']))
        else:
            name = request.form['name']
            capacity = request.form['capacity']
            rtype = request.form['type']
            location = request.form['location']
            Room.add_room(name, capacity, rtype, location)
            flash('Room added.', 'success')
    rooms = Room.get_all_rooms()
    return render_template('admin_rooms.html', rooms=rooms)

@admin_bp.route('/rooms/<int:room_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_room(room_id):
    room = Room.get_room_by_id(room_id)
    if request.method == 'POST':
        name = request.form['name']
        capacity = request.form['capacity']
        rtype = request.form['type']
        location = request.form['location']
        Room.update_room(room_id, name, capacity, rtype, location)
        flash('Room updated.', 'success')
        return redirect(url_for('admin.manage_rooms'))
    return render_template('admin_edit_room.html', room=room)

@admin_bp.route('/timeslots', methods=['GET', 'POST'])
@admin_required
def manage_timeslots():
    if request.method == 'POST':
        if 'delete' in request.form:
            Timeslot.delete_timeslot(request.form['slot_id'])
            flash('Timeslot deleted.', 'success')
        elif 'edit' in request.form:
            # redirect to edit page
            return redirect(url_for('admin.edit_timeslot', slot_id=request.form['slot_id']))
        else:
            date = request.form['date']
            start = request.form['start']
            end = request.form['end']
            Timeslot.add_timeslot(date, start, end)
            flash('Timeslot added.', 'success')
            
    slots = Timeslot.get_all_timeslots()
    return render_template('admin_timeslots.html', slots=slots)

@admin_bp.route('/timeslots/<int:slot_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_timeslot(slot_id):
    timeslot = Timeslot.get_timeslot_by_id(slot_id)
    if request.method == 'POST':
        date = request.form['date']
        start = request.form['start']
        end = request.form['end']
        Timeslot.update_timeslot(slot_id, date, start, end)
        flash('Timeslot updated.', 'success')
        return redirect(url_for('admin.manage_timeslots'))
    return render_template('admin_edit_timeslot.html', timeslot=timeslot)

@admin_bp.route('/users')
@admin_required
def manage_users():
    users = User.get_all_users()
    return render_template('admin_users.html', users=users)

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if User.create_user(name, email, password, role):
            flash('User created successfully.', 'success')
            return redirect(url_for('admin.manage_users'))
        else:
            flash('Error creating user. Email may already exist.', 'danger')
    
    return render_template('admin_user_form.html', user=None, action='Create')

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.get_user_by_id(user_id)
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form.get('password', '').strip()
        role = request.form['role']
        
        # Only update password if provided
        if User.update_user(user_id, name=name, email=email, 
                           password=password if password else None, role=role):
            flash('User updated successfully.', 'success')
            return redirect(url_for('admin.manage_users'))
        else:
            flash('Error updating user.', 'danger')
    
    return render_template('admin_user_form.html', user=user, action='Edit')

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    # Prevent deleting yourself
    if user_id == session.get('user_id'):
        flash('Cannot delete your own account.', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    if User.delete_user(user_id):
        flash('User deleted successfully.', 'success')
    else:
        flash('Error deleting user.', 'danger')
    
    return redirect(url_for('admin.manage_users'))
