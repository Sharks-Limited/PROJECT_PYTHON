from flask import  render_template, redirect, request, flash,session
from flask_app import app
from flask_app.models.day import Day
from flask_app.models.exercise import Exercise
from datetime import datetime


@app.route('/days/<int:program_id>/plan_your_week')
def plan_week(program_id):
    all_days = Day.get_all_prog_days({'id':program_id})
    # print(all_days)
    for day in all_days:
        print(day.body_name_day)
        exercices = Exercise.get_all_days_exercices({'day_id':day.id})
        # print("😊😊😊😊😊😊😂😊🤣😂🤣🤣", exercices)
        if exercices!=False:
            for exercice in exercices:
                day.exercices.append(exercice)
        # print("***************************")
    return render_template('plan_your_week.html',days=all_days)