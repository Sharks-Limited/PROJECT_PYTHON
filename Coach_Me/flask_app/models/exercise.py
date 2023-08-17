from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE_NAME
from datetime import datetime
from flask import flash

class Exercise:
    def __init__(self, data_dict) :
        self.id = data_dict['id']
        self.coach_id = data_dict['coach_id']
        self.exercice_name = data_dict['exercice_name']
        self.num_of_series = data_dict['num_of_series']
        self.num_of_reps = data_dict['num_of_reps']
        self.exercice_picture = data_dict['exercice_picture']
        self.description = data_dict['description']
        self.created_at = data_dict['created_at']
        self.updated_at = data_dict['updated_at']
        
    @classmethod
    def create_exercise(cls,data_dict):
        query="""INSERT INTO exercices 
                (coach_id,exercice_name,num_of_series,num_of_reps,exercice_picture,description)
                VALUES (%(coach_id)s,%(exercice_name)s,%(num_of_series)s
                ,%(num_of_reps)s,%(exercice_picture)s,%(description)s);"""
        return connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
    
    @classmethod
    def create_day_exercise(cls,data_dict):
        query="""INSERT INTO exercices_has_days 
                (exercice_id,day_id)
                VALUES (%(exercice_id)s,%(day_id)s);"""
        return connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
    
    @classmethod
    def get_all_days_exercices(cls,data_dict):
        query="""SELECT * from exercices
                    join exercices_has_days on exercices.id = exercices_has_days.exercice_id
                    join days on days.id = exercices_has_days.day_id
                    where days.id=%(day_id)s;"""
        results = connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
        exer = []
        if not results:
            # print("👍👍👍👍👍👍👍👍👍",results,"👍👍👍👍👍👍👍👍👍")
            return False
        for row in results:
            exercices = cls(row)
            exer.append(exercices)
        return exer
    
    @staticmethod
    def validate(data_dict):
        is_valid=True
        if len(data_dict['exercice_name'])=="":
            flash("Exercise name is required", "exercice_name")
            is_valid = False
        elif len(data_dict['exercice_name'])<2:
            flash("Exercise name too short", "exercice_name")
            is_valid = False
            
        if len(data_dict['num_of_series'])=="":
            flash("Number of series is required", "num_of_series")
            is_valid = False
            
        if len(data_dict['num_of_reps'])=="":
            flash("Number of repetitions too short", "num_of_reps")
            is_valid = False
        
        if len(data_dict['description'])=="":
            flash("Description too short", "description")
            is_valid = False
        elif len(data_dict['description'])<2:
            flash("Description too short", "description")
            is_valid = False
            
        return is_valid