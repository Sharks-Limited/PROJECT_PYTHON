# Import necessary modules and libraries
from decimal import Decimal, ROUND_HALF_UP
from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.bmi import Bmi
from flask_app.models.program import Program
from flask_app.models.user_measure import User_measure
from flask_bcrypt import Bcrypt
from math import sqrt

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)


# Define route for the homepage
@app.route('/')
def index():
    return render_template("landing_page.html")

# Define route for the Login and registration
@app.route('/reg_log')
def reg_log():
    return render_template("reg_log.html")

# Define route for the coach dashboard
@app.route('/dashboard_coach')
def dashboard_coach():
    # Check user role and session status
    if 'user_id' not in session:
        return redirect('/')
    if session['role'] != "c":
        return redirect('/')
    
    # Get the logged-in user's information
    logged_user = User.get_by_id({'id': session['user_id']})
    coach_programs= Program.get_all_coach_program({'id': session['user_id']})
    for program in coach_programs:
        enrolled_user = Program.get_enrolled({'program_id':program.id})
        if enrolled_user!=False:
            for enrolled in enrolled_user:
                print (enrolled)
                program.enrolled.append(enrolled['num_enrolled'])


    return render_template("dashboard_coach.html", user=logged_user, programs=coach_programs)

# Define route for the user dashboard


@app.route('/dashboard_user')
def dashboard_user():
    # Check user role and session status
    if session['role'] != "u" or 'user_id' not in session:
        return redirect('/')
    # Get the logged-in user's information
    logged_user = User.get_by_id({'id': session['user_id']})
    bmi_user = User_measure.get_bmi({'user_id':logged_user.id})
    all_coaches_by_bmi_program = Program.get_coaches_by_bmi_program({'bmi_id':bmi_user.bmi_id})
    return render_template("dashboard_user.html", user=logged_user, all_programs= all_coaches_by_bmi_program)



# Define route for the admin dashboard
@app.route('/dashboard_admin')
def dashboard_admin():
    # Check user role and session status
    if 'user_id' not in session:
        return redirect('/')
    if session['role'] != "a":
        return redirect('/')
    # Get the logged-in user's information
    logged_user = User.get_by_id({'id': session['user_id']})
    invalid_coachs = User.get_invalid_coachs()
    valid_coachs = User.get_valid_coachs()
    users = User.get_all_users()
    return render_template("dashboard_admin.html",users=users,valid_coachs=valid_coachs,invalid_coachs=invalid_coachs, user=logged_user)

# Define route for user registration
@app.route('/users/create', methods=['POST'])
def register():
    pic=""
    # Validate user registration form data
    if User.validate_register(request.form):
        uploaded_file = request.files['file']
        
        # Handle uploaded profile picture
        if request.form['role'] in ["c", "u"] and uploaded_file.filename == "":
            flash("Please provide your picture", "file")
            return redirect('/reg_log')
            
        
        if request.form['role'] in ["c", "u"] and uploaded_file.filename != "":
            pic = 'flask_app/static/img/' + uploaded_file.filename
            uploaded_file.save(pic)
        
        # Hash the password and set validation status
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        if request.form['role'] == "c":
            is_valid = 0
        else:
            is_valid = 1
        
        # Create user data dictionary
        data_dict = {
            **request.form,
            'password': pw_hash,
            'picture': pic,
            'is_valid': is_valid
        }
        
        # Create user and handle BMI calculation if applicable
        user_id = User.create_user(data_dict)
        if request.form['role'] == "u":
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            user_bmi = round(weight / ((height / 100) ** 2), 2)
            
            bmis = Bmi.get_all_bmis()
            for thebmi in bmis:
                if thebmi.min_range < user_bmi < thebmi.max_range:
                    data_measures = {
                        'user_id': user_id,
                        'bmi_id': thebmi.id,
                        'height': Decimal(height).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
                        'weight': Decimal(weight).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
                        'bmi': Decimal(user_bmi).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                    }
            User_measure.create_user_measure(data_measures)
        
        # Set session information and redirect based on role
        session['user_id'] = user_id
        session['user_first_name'] = request.form['first_name']
        session['role'] = request.form['role']
        if request.form['role'] == "c":
            return redirect('/dashboard_coach')
        if request.form['role'] == "u":
            return redirect('/dashboard_user')
        if request.form['role'] == "a":
            return redirect('/dashboard_admin')
    # Redirect back to the homepage if form validation fails
    return redirect('/reg_log')

# Define route for user login
@app.route('/login', methods=['POST'])
def login():
    # Get user data from the database based on provided email
    user_from_db = User.get_by_email({'email': request.form['email']})
    if user_from_db:
        # Check password and set session information if valid
        if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
            flash("Incorrect email or password. Please try again.", "login")
            return redirect('/reg_log')
        session['user_id'] = user_from_db.id
        session['role'] = user_from_db.role
        session['user_first_name'] = user_from_db.first_name
        if user_from_db.role == "c":
            return redirect('/dashboard_coach')
        if user_from_db.role == "u":
            return redirect('/dashboard_user')
        if user_from_db.role == "a":
            return redirect('/dashboard_admin')
    flash("Incorrect email or password. Please try again.", "login")
    return redirect('/reg_log')

@app.route('/users/validate',methods=['POST'])
def validate_coach():
    if 'user_id' not in session:

        return redirect('/')
    
    if session['role'] != "a":
        return redirect('/')
    User.validate_coach({'id':request.form['coach_id']})
    return redirect('/dashboard_admin')

@app.route('/users/validate',methods=['POST'])
def block_coach():
    if 'user_id' not in session:
        return redirect('/')
    
    if session['role'] != "a":
        return redirect('/')
    User.validate_coach({'id':request.form['coach_id']})
    return redirect('/dashboard_admin')


@app.route('/users/delete',methods=['POST'])
def delete_coach():
    if 'user_id' not in session:
        return redirect('/')
    User.delete_coach({'id':request.form['coach_id']})
    return redirect('/dashboard_admin')
# Define route for user logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')




#=====================routes for admin page ===========================


#===========ban a coach=======
@app.route('/coachs/ban',methods=['POST'])

def ban():

    if 'user_id' not in session:

        return redirect('/')
    
    if session['role'] != "a":
        return redirect('/')
    
    

    User.ban_coach({'id':request.form['coach_id']})
    return redirect('/dashboard_admin')


#===========     unban a coach  =======
    

@app.route('/coachs/unban',methods=['POST'])

def unban():

    if 'user_id' not in session:

        return redirect('/')
    
    if session['role'] != "a":
        return redirect('/')
    
    

    User.unban_coach({'id':request.form['coach_id']})
    return redirect('/dashboard_admin')

    





#=====================routes for Coach page ===========================


#=======edit coach get================
@app.route('/edit_coach')
def edit_coach():
    logged_user = User.get_by_id({'id': session['user_id']})
    return render_template("edit_coach.html",user=logged_user)




#==================edit coach redirect to get
@app.route('/coach/edit', methods=['POST'])
def edit():
    if 'user_id' not in session:
        return redirect('/')
    
    if session['role'] != "c":
        return redirect('/')
    return redirect("/edit_coach")

# programs=coach_programs

@app.route('/coach/update', methods=['POST'])
def update_coach():
    if 'user_id' not in session:
        return redirect('/')
    if not User.coach_validate_update(request.form):
        return redirect('/edit_coach')
    uploaded_file = request.files['file']
    if uploaded_file.filename == "":
        flash("Please provide your picture", "file")
        return redirect('/')
    pic = 'flask_app/static/img/' + uploaded_file.filename
    uploaded_file.save(pic)
    print(request.form)
    
    data= {
            **request.form,
            'picture': pic,
            'id':session['user_id']
        }
    
    User.update_coach(data)
    return redirect('/dashboard_coach')


# @app.route('/coachs/block', methods=['POST'])
# def block_coach():
#     coach_to_block_ = User.Block(request.form['coach_id'])
    