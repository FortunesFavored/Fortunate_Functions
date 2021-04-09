from app import App
from flask import render_template, request, flash, redirect, url_for
from app.forms import LineVariables, BellVariables, DataFile, Equation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from IPython.display import HTML
import io
import base64
import re


@App.route('/', methods = ['GET', 'POST'])
@App.route('/index', methods = ['GET', 'POST'])
def index():
    title = 'HOME'
    form = Equation()
    
    if request.method =='POST' and form.equation.data != '' and re.findall("[^x0-9\^\/\*\-\+]",form.equation.data) == []:
        homeGraph = plotCustomEquation(form.equation.data)
        return render_template('index.html', title=title,form=form, image=homeGraph)

    return render_template('index.html', title=title, form=form)

@App.route('/graph', methods = ['GET', 'POST'])
def graph():
    title = 'Custom Data'
    Data = DataFile()
    if request.method =='POST' and request.files['file'].filename != '':
        try:
            data = pd.read_csv(Data.file.data, delimiter=',')
            html_table = [data.to_html(classes='data')]
        except:
            return render_template('graph.html', title=title, data=Data, error='File not Supported')
        return render_template('graph.html', title=title, data=Data, tables=[data.to_html(classes='data')], titles=data.columns.values)
    return render_template('graph.html', title=title, data=None)



@App.route('/newplot', methods = ['GET', 'POST'])
def newplot():
    title = 'New Plot'
    form1 = LineVariables()
    form2 = BellVariables()
    linImg = plotXView()
    bellImg = plotBView()
    if request.method == 'POST' and (form1.intercept.data != None or form1.slope.data != None):
        lin_b = form1.intercept.data
        lin_m = form1.slope.data
        linImg = plotXView(lin_b, lin_m)
        return render_template('newplot.html', title=title, form1=form1, form2=form2, linImg=linImg, bellImg=bellImg)
    if request.method == 'POST' and (form2.sq_a.data != None or form2.sq_b != None or form2.sq_c != None):
        sq_a = form2.sq_a.data
        sq_b = form2.sq_b.data
        sq_c = form2.sq_c.data
        bellImg = plotBView(sq_a, sq_b, sq_c)
        return render_template('newplot.html', title=title, form1=form1 , form2=form2, linImg=linImg, bellImg=bellImg)
    return render_template('newplot.html', title=title, form1=form1 , form2=form2, linImg=linImg, bellImg=bellImg)

### For file uploads look into reading the csv/txt

    


def plotXView(intercept=0, aSlope=1):
    # Generate plot
    if intercept == None: intercept=0
    if aSlope == None: aSlope = 1
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("")
    axis.set_xlabel("x-axis")
    axis.set_xlim([-10,10])
    axis.set_ylabel("y-axis")
    axis.set_ylim([-10,10])
    axis.grid()
    axis.plot(np.arange(-11, 12, 0.1), [(aSlope*x + intercept) for x in np.arange(-11, 12, 0.1)], "ro-")
    
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    return pngImageB64String

def plotBView(a=1, b=1, c=0):
    # Generate plot
    if a == None: a = 1
    if b == None: b = 0
    if c == None: c = 0
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("")
    axis.set_xlabel("x-axis")
    axis.set_xlim([-10,10])
    axis.set_ylabel("y-axis")
    if a < 0: axis.set_ylim([a*(100),a*(-10)])
    else: axis.set_ylim([-10,100,])
    axis.grid()
    axis.plot(np.arange(-11, 12, 0.1), [(a*(x**2) + (b*x) + c) for x in np.arange(-11, 12, 0.1)], "ro-")
    
    # Convert plot to PNG image
    bellImg = io.BytesIO()
    FigureCanvas(fig).print_png(bellImg)
    
    # Encode PNG image to base64 string
    bellImgB64String = "data:image/png;base64,"
    bellImgB64String += base64.b64encode(bellImg.getvalue()).decode('utf8')
    
    return bellImgB64String

def plotCustomEquation(eqString, xAxis=np.arange(-11,11,0.1)):
    # Generate plot
    plt.xlim(-10,10)
    plt.ylim(-10,10)
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("")
    axis.set_xlabel("x-axis")
    axis.set_ylabel("y-axis")
    axis.grid()
    yAxis = equationSolver(eqString, xAxis)
    axis.plot(xAxis, yAxis, "ro-")
    
    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    # Encode PNG image to base64 string
    homeGraph = "data:image/png;base64,"
    homeGraph += base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    return homeGraph



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
    return [eval(finalEquation) for x in xlist]