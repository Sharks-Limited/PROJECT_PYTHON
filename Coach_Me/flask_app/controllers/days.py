from flask import  render_template, redirect, request, flash,session
from flask_app import app
from flask_app.models.day import Day
from datetime import datetime


@app.route('/days/<int:program_id>/plan_your_week')
def plan_week(program_id):
    all_days_program = Day.get_all_prog_days({'program_id':program_id})
    return render_template('plan_your_week.html',all_days=all_days_program)