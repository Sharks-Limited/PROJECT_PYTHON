from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE_NAME
from flask_app.models.day import Day
from flask_app.models.bmi import Bmi
from datetime import datetime
from flask import flash

class Program:
    def __init__(self, data_dict) :
        self.id = data_dict['id']
        self.coach_id = data_dict['coach_id']
        self.bmi_id = data_dict['bmi_id']
        self.name_of_program = data_dict['name_of_program']
        self.description_of_program = data_dict['description_of_program']
        self.duration = data_dict['duration']
        self.created_at = data_dict['created_at']
        self.updated_at = data_dict['updated_at']
        self.bmi={}
        self.category_name=""
        self.days = []
    
    @classmethod
    def get_all_programs(cls):
        query="""SELECT * from programs;"""
        results = connectToMySQL(DATABASE_NAME).query_db(query)
        programs = []
        for row in results:
            program = cls(row)
            programs.append(program)
        return programs
        
    @classmethod
    def create_program(cls,data_dict):
        query="""INSERT INTO programs (coach_id,bmi_id,name_of_program,description_of_program,duration)
                VALUES (%(coach_id)s,%(bmi_id)s,%(name_of_program)s,%(description_of_program)s,%(duration)s)"""
        return connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
    
    
    @classmethod
    def get_all_coach_program(cls,data_dict):
        query="""SELECT * from programs 
                    join users on users.id=programs.coach_id
                    join bmis on bmis.id =programs.bmi_id
                    where coach_id=%(id)s;"""
        results = connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
        programs = []
        for row in results:
            
            program = cls(row)
            program.category_name=row['category_name']
            programs.append(program)
        return programs
    
    @classmethod
    def get_details_coach_program(cls,data_dict):
        query="""SELECT * from programs
                    join bmis on bmis.id = programs.bmi_id
                    join days on days.program_id =programs.id
                    where programs.id=%(id)s"""
        results = connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
        program = cls(results[0])
        program.category_name = results[0]['category_name']
        for row in results:
            data_days ={
                'id':row['days.id'],
                'program_id':row['program_id'],
                'body_name_day':row['body_name_day'],
                'day_off':row['day_off'],
                'created_at':row['created_at'],
                'updated_at':row['updated_at']
            }
            
            program.days.append(Day(data_days))
        return program
    
    @classmethod
    def get_details_coach_program_for_edit(cls,data_dict):
        query="""SELECT * from programs
                    join bmis on bmis.id = programs.bmi_id
                    join days on days.program_id =programs.id
                    where programs.id=%(id)s"""
        results = connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
        program = cls(results[0])
        program.bmi = {
            'id':results[0]['bmis.id'],
            'min_range':results[0]['min_range'],
            'max_range':results[0]['max_range'],
            'category_name':results[0]['category_name']
            } 
        for row in results:
            data_days ={
                'id':row['days.id'],
                'program_id':row['program_id'],
                'body_name_day':row['body_name_day'],
                'day_off':row['day_off'],
                'created_at':row['days.created_at'],
                'updated_at':row['days.updated_at']
            }
            program.days.append(Day(data_days))
        return program
    
    @classmethod
    def get_one_program(cls,data_dict):
        query="""SELECT * from programs
                    where id=%(id)s"""
        results = connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
        prog = cls(results[0])
        return prog
    
    @staticmethod
    def validate_program(data_dict):
        is_valid = True
        if len(data_dict['program_name'])< 2:
            flash("Name of program is too short", "program_name")
            is_valid = False
        if data_dict['bmi']=="":
            flash("please provide a category", "bmi")
            is_valid = False
        if len(data_dict['duration'])==0:
            flash("please put a positive number", "duration")
            is_valid = False
        # if len(data_dict['duration'])==:
        #     flash("please put a positive number", "duration")
        #     is_valid = False
        if len(data_dict['description'])<7:
            flash("the description must be more the 7 characters", "description")
            is_valid = False
        # if data_dict['day_1']=="":
        #     flash("this day required", "day_1")
        #     is_valid = False
        # elif len(data_dict['day_1'])<2:
        #     flash("the day must be more the 2 characters", "day_1")
        #     is_valid = False
        # if data_dict['day_2']=="":
        #     flash("this day required", "day_2")
        #     is_valid = False
        # elif len(data_dict['day_2'])<2:
        #     flash("the day must be more the 2 characters", "day_2")
        #     is_valid = False
        # if data_dict['day_3']=="":
        #     flash("this day required", "day_3")
        #     is_valid = False 
        # elif len(data_dict['day_3'])<2:
        #     flash("the day must be more the 2 characters", "day_3")
        #     is_valid = False
        # if data_dict['day_4']=="":
        #     flash("this day required", "day_4")
        #     is_valid = False  
        # elif len(data_dict['day_4'])<2:
        #     flash("the day must be more the 2 characters", "day_4")
        #     is_valid = False
        # if data_dict['day_5']=="":
        #     flash("this day required", "day_5")
        #     is_valid = False
        # elif len(data_dict['day_5'])<2:
        #     flash("the day must be more the 2 characters", "day_5")
        #     is_valid = False
        # if data_dict['day_6']=="":
        #     flash("this day required", "day_6")
        #     is_valid = False 
        # elif len(data_dict['day_6'])<2:
        #     flash("the day must be more the 2 characters", "day_6")
        #     is_valid = False
        # if data_dict['day_7']=="":
        #     flash("this day required", "day_7")
        #     is_valid = False
        # elif len(data_dict['day_7'])<2:
        #     flash("the day must be more the 2 characters", "day_7")
        #     is_valid = False
        return is_valid

    
    @classmethod
    def update_program(cls,data_dict):
        query= """UPDATE programs SET bmi_id=%(bmi_id)s,name_of_program=%(name_of_program)s,
                    description_of_program=%(description_of_program)s,
                    duration=%(duration)s WHERE id=%(id)s"""
                    
        return connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
    
    @classmethod
    def delete(cls,data_dict):
        query = """delete from recipes where id=%(id)s"""
        return connectToMySQL(DATABASE_NAME).query_db(query,data_dict)