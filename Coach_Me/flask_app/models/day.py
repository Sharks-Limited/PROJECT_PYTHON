from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE_NAME
from datetime import datetime
from flask import flash

class Day:
    def __init__(self, data_dict) :
        self.id = data_dict['id']
        self.program_id = data_dict['program_id']
        self.body_name_day = data_dict['body_name_day']
        self.day_off = data_dict['day_off']
    
    @classmethod
    def get_all_days(cls):
        query="""SELECT * from days;"""
        results = connectToMySQL(DATABASE_NAME).query_db(query)
        days = []
        for row in results:
            day = cls(row)
            days.append(day)
        return days
        
    
    @classmethod
    def get_one_day(cls,data_dict):
        query="""SELECT * from days
                    where id=%(id)s"""
        results = connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
        days = cls(results[0])
        return days
    
    @classmethod
    def get_all_prog_days(cls,data_dict):
        query="""SELECT * from days where program_id=%(program_id)s;"""
        results = connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
        days = []
        for row in results:
            day = cls(row)
            days.append(day)
        return days
        
    
    @classmethod
    def create_program_days(cls,data_dict):
        query="""INSERT INTO days (program_id,body_name_day,day_off)
                VALUES (%(program_id)s,%(body_name_day)s,%(day_off)s)"""
        return connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
    
    @classmethod
    def update_program_days(cls,data_dict):
        query= """UPDATE days 
                    SET body_name_day=%(body_name_day)s,day_off=%(day_off)s 
                    WHERE program_id=%(program_id)s and id=%(id)s"""
                    
        return connectToMySQL(DATABASE_NAME).query_db(query,data_dict)
    