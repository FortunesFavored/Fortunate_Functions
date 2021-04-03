from app import App
# , db, mail, Message
from flask import render_template, request, flash, redirect, url_for
from app.forms import Variables, DataFile
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


@App.route('/')
@App.route('/index')
def index():
    title = 'HOME'
    return render_template('index.html', title=title)

@App.route('/graph', methods = ['GET', 'POST'])
def graph():
    title = 'HOME'
    pngImageB64String = plotView()
    return render_template('graph.html', title=title, image=pngImageB64String)

@App.route('/newplot', methods = ['GET', 'POST'])
def newplot():
    title = 'New Plot'
    form = Variables()
    if request.method == 'POST':
        form = Variables()
        pngImageB64String = plotView(form.exponent.data, form.slope.data)
        return render_template('graph.html', title=title, image=pngImageB64String, slope=form.slope.data, exp=form.exponent.data)
    return render_template('newplot.html', title=title, form=form)

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
