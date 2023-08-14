from flask import  render_template, redirect, request, flash,session
from flask_app import app
from flask_app.models.day import Day
from datetime import datetime