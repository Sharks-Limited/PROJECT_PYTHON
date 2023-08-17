from flask_app import app

# ! Don't forget to import all controllers here 
from flask_app.controllers import users,user_measures,programs,days, exercises


if __name__ == '__main__':
    app.run(debug=True,port=5000)