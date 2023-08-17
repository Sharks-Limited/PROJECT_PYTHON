# Import necessary modules and libraries
from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.program import Program
from flask_app.models.user import User
from flask_app.models.bmi import Bmi
from flask_app.models.day import Day
from datetime import datetime, timedelta

# Define route for creating a new program
@app.route('/programs/new')
def program_new():
    # Check user session and role
    if not 'user_id' in session:
        return redirect('/')
    
    if session['role'] != 'c':
        return redirect('/')
    
    # Get all BMI categories for dropdown
    categories = Bmi.get_all_bmis()
    return render_template("create_program.html", bmis=categories)

# Define route for creating a new program
@app.route('/programs/create', methods=['POST'])
def create_program():
    # Check user session and role
    if not 'user_id' in session:
        return redirect('/')
    if session['role'] != 'c':
        return redirect('/')
    
    # Validate program form data
    if Program.validate_program(request.form):
        data_program = {
            'coach_id': session['user_id'],
            'bmi_id': request.form['bmi'],
            'name_of_program': request.form['program_name'],
            'description_of_program': request.form['description'],
            'duration': request.form['duration'],
        }
        
        # Create a new program
        program_id = Program.create_program(data_program)
        #Loop through days and create program days
        for i in range(1, 8):
            if f'day_off_{i}' in request.form:
                day_off = 1
            else:
                day_off = 0
            
            if f'day_{i}' not in request.form:
                day_name = ''
            else:
                day_name = request.form[f'day_{i}']
            data_days = {
                'program_id': program_id,
                'body_name_day': day_name,
                'day_off': day_off,
            }
            Day.create_program_days(data_days)
        return redirect(f'/programs/view/{program_id}')
    
    # Redirect back to program creation page if validation fails
    return redirect('/programs/new')

# Define route for viewing program details
@app.route('/programs/view/<int:program_id>')
def details_program(program_id):
    # Check user session
    if not 'user_id' in session:
        return redirect('/')
    if session['role'] != 'c':
        return redirect('/')
    
    # Get user program details and logged-in user's information
    coach_program = Program.get_details_coach_program({'id': program_id})
    return render_template('details_program.html', program=coach_program)

# Define route for editing a program
@app.route('/programs/<int:program_id>/edit')
def edit_program(program_id):
    # Check user session
    if 'user_id' not in session:
        return render_template('/')
    if session['role'] != 'c':
        return redirect('/')
    
    # Get program details for editing
    coach_program = Program.get_details_coach_program_for_edit({'id': program_id})
    bmis = Bmi.get_bmis_not_in_program({'id': program_id})
    return render_template('edit_program.html',bmis=bmis, program=coach_program)

# Define route for updating a program
@app.route('/programs/<int:program_id>/update', methods=['POST'])
def update_program(program_id):
    if 'user_id' not in session:
        return render_template('/')
    if session['role'] != 'c':
        return redirect('/')
    if Program.validate_program(request.form):
        data_program = {
            'id': program_id,
            'name_of_program': request.form['program_name'],
            'description_of_program': request.form['description'],
            'duration': request.form['duration'],
        }
        # Update program details
        Program.update_program(data_program)
        days = Day.get_all_prog_days({'program_id':program_id})
        
        for i, day in enumerate(days, start=1):
            
            if f'day_off_{i}' in request.form:
                day_off = 1
            else:
                day_off = 0
            data_days = {
                'id':day.id,
                'program_id': program_id,
                'body_name_day': request.form[f'day_{i}'],
                'day_off': day_off,
            }
            Day.update_program_days(data_days)
        return redirect('/dashboard_coach')
    return redirect(f"/programs/view/{program_id}")

# Define route for deleting a program
@app.route('/programs/<int:user_programs_id>/destroy', methods=['POST'])
def delete(user_programs_id):
    # Delete a program
    Program.delete({'id': user_programs_id})
    return redirect('/programs')



    