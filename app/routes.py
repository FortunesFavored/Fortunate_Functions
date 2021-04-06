from app import App
# , db, mail, Message
from flask import render_template, request, flash, redirect, url_for
from app.forms import Variables, DataFile, Equation
# from app.models import User, Plans, Cart
# from flask_login import login_user, logout_user, login_required, current_user
# from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import base64


@App.route('/', methods = ['GET', 'POST'])
@App.route('/index', methods = ['GET', 'POST'])
def index():
    title = 'HOME'
    form = Equation()
    if request.method =='POST' and form.equation.data != '':
        pngImageB64String = plotCustomEquation(form.equation.data)
        return render_template('index.html', title=title,form=form, image=pngImageB64String)
    pngImageB64String = plotView()
    return render_template('index.html', title=title, form=form)

@App.route('/graph', methods = ['GET', 'POST'])
def graph():
    title = 'Custom Data'
    Data = DataFile()
    if request.method =='POST' and request.files['file'].filename != '':
        return render_template('graph.html', title=title, data=Data)
    return render_template('graph.html', title=title, data=None)

@App.route('/newplot', methods = ['GET', 'POST'])
def newplot():
    title = 'New Plot'
    form = Variables()
    if request.method == 'POST':
        pngImageB64String = plotView(form.exponent.data, form.slope.data)
        return render_template('newplot.html', title=title, form=form, image=pngImageB64String, slope=form.slope.data, exp=form.exponent.data)
    pngImageB64String = plotView()
    return render_template('newplot.html', title=title, form=form, image=pngImageB64String)

### For file uploads look into reading the csv/txt

    


def plotView(exponent=1, aSlope=1):
    # Generate plot
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("title")
    axis.set_xlabel("x-axis")
    axis.set_ylabel("y-axis")
    axis.grid()
    axis.plot(range(-20, 21), [aSlope*x**exponent for x in range(-20, 21)], "ro-")
    
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    return pngImageB64String

def plotCustomEquation(eqString, xAxis=range(-20,20)):
    # Generate plot
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("title")
    axis.set_xlabel("x-axis")
    axis.set_ylabel("y-axis")
    axis.grid()
    yAxis = equationSolver(eqString, xAxis)
    axis.plot(xAxis, yAxis, "ro-")
    
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    return pngImageB64String

def equationSolver(eqString, xlist):
    parsedEquation = list(eqString)
    pointer = 0
    eqLen = len(parsedEquation)
    while pointer < eqLen:
        if parsedEquation[pointer] == '^':
            parsedEquation[pointer] = '**'
        try:
            if parsedEquation[pointer].isdigit() and (parsedEquation[pointer+1] == 'x' or parsedEquation[pointer+1] == '('):
                parsedEquation.insert(pointer+1,'*')
            if parsedEquation[pointer] == ')' and (parsedEquation[pointer+1] == 'x' or parsedEquation[pointer+1].isdigit()):
                parsedEquation.insert(pointer+1,'*')
        except:
            pass
        eqLen = len(parsedEquation)
        pointer += 1
    finalEquation = ''.join(parsedEquation)
    print(finalEquation)
    return [eval(finalEquation) for x in xlist]