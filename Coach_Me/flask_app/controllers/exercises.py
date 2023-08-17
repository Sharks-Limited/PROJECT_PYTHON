from flask import  render_template, redirect, request, flash,session
from flask_app import app
from flask_app.models.exercise import Exercise
from flask_app.models.user import User
from datetime import datetime


@app.route('/exercises/<int:day_id>/new',methods=['POST'])
def create_exercise(day_id):
    if 'file' not in request.files:
        flash('please put a gif picture','file')
        return redirect(f'days/{day_id}/plan_your_week#edit_delete_exercice')
    else:
        uploaded_file = request.files['file']
        pic = 'flask_app/static/img/' + uploaded_file.filename
        uploaded_file.save(pic)
    if Exercise.validate(request.form):
        print("*************************************")
        logged_user = User.get_by_id({'id': session['user_id']})
        data_dict = {
            **request.form,
            'coach_id':logged_user.id,
            'exercice_picture':pic
        }
        exrcice_id = Exercise.create_exercise(data_dict)
        data_day_exercise={
            'exercice_id':exrcice_id,
            'day_id':day_id
        }
        Exercise.create_day_exercise(data_day_exercise)
        id= session['program_id']
    # Get program details for editing
    # coach_program = Program.get_details_coach_program_for_edit({'id': program_id})
    # bmis = Bmi.get_bmis_not_in_program({'id': program_id})
    return redirect(f'/days/{id}/plan_your_week')
