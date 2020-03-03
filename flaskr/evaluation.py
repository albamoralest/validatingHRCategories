from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.mngmt.DataManagement import DataManagement
#from flaskr.db import get_db

bp = Blueprint('evaluation', __name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    posts=""
    
    #setting a number of samples the user will evaluate
    res = DataManagement()
    sample='1'
    res.setDirectory(sample)
    
    #returns a random list of IDs 
    sampleList = res.returnRandomSample()
    sampleNumber=len(sampleList)
    q1percentage=None
    q2percentage=None
    
    #Verify if the user already has answered the question
    username = g.user['username']
    userFile = res.loadUserFile(username)
    if userFile['q1']['total'] == 0:
        q1percentage = None
        labelq1 = "Click to start"
    elif userFile['q1']['total'] == sampleNumber:
        q1percentage = 100
        labelq1 = "Completed"
    else:
        q1percentage = round((userFile['q1']['total']*100)/sampleNumber)
        labelq1 = "Click to continue"

    res.setDirectory('2')
    sampleList = res.returnRandomSample()
    sampleNumber=len(sampleList)
    if userFile['q2']['total'] == 0:
        q2percentage = None
        labelq2 = "Click to start"
    elif userFile['q2']['total'] == sampleNumber:
        q2percentage = 100
        labelq2 = "Completed"
    else:
        q2percentage = round((userFile['q2']['total']*100)/sampleNumber)
        labelq2 = "Click to continue"
        
    return render_template('eval/index.html', totalsample=sampleNumber,q1number=q1percentage,
                           q2number=q2percentage,
                           labelq1=labelq1,labelq2=labelq2,posts=posts)


@bp.route('/question1', methods=('GET', 'POST'))
@bp.route('/eval/question1', methods=('GET', 'POST'))
@login_required
def question1():
    sample='1'
    #setting a number of samples the user will evaluate
    res = DataManagement()
    
    res.setDirectory(sample)
    #Verify if the user already has answered the question
    username = g.user['username']
    userFile = res.loadUserFile(username)
        
    if request.method == 'POST':
        error=None
        if request.form.get('inlineRadioOptions') == 'option1':
            answerValue = 'YES'
        elif request.form.get('inlineRadioOptions') == 'option2':
            answerValue = 'NO'
        else:
            error = "Please provide an answer."
        
        if error is None:
            #save the results
            patientID =request.form.get('patient')
            value = " "
            rowValues = [username,'Q1',patientID,answerValue, value]
            res.appendRowsCSVresultsFile(username, rowValues)
            #update session values
            userFile['q1']['total'] = 1+userFile['q1']['total']
            userFile['q1']['current'] = patientID
            res.updateUserFile(username, userFile)
        else:
            flash(error)
    
    #returns a random list of IDs 
    sampleList = res.returnRandomSample()
    sampleNumber=len(sampleList)
    
    #query the number
    if userFile['q1']['total'] == 0:
        left = sampleNumber 
        patientID = sampleList[0]
    elif userFile['q1']['total'] == sampleNumber:
        #the user has reached the max sample number
        return redirect(url_for('index'))
    else:
        left = sampleNumber - userFile['q1']['total']
        patientID=userFile['q1']['current']
        #find the index of the actual value and select the next ID
        j = 0
        for i in sampleList:
            i = i.replace(".json","")
            j+=1
            if i == patientID:
                print(i)
                break 
        patientID=sampleList[j]
        print(patientID)
    patient = res.loadSampleFile(patientID)

    patientID = patientID.replace(".json","")
    patientDetails = patient['patient']['details']
    
    patientRelevantInf = patient['patient']['informativeData']
        
    return render_template('eval/question1.html', patientid=patientID,sample=sample, total=sampleNumber, 
                           left=left, 
                           title='Question 1', details=patientDetails,relevant=patientRelevantInf)


@bp.route('/question2', methods=('GET', 'POST'))
def question2():
    
    sample='2'
    #setting a number of samples the user will evaluate
    res = DataManagement()
    
    res.setDirectory(sample)
    #Verify if the user already has answered the question
    username = g.user['username']
    userFile = res.loadUserFile(username)
        
    if request.method == 'POST':
        error=None
        print(request.form.get('category'))
        if request.form.get('category') != '00':
            answerValue = request.form.get('category')
        else:
            error = "Please select a Category from the list."
            
        if error is None:
            #save the results
            patientID =request.form.get('patient')
            cat = res.obtainCategoryName(answerValue)
            rowValues = [username,'Q2',patientID,answerValue,cat]
            res.appendRowsCSVresultsFile(username, rowValues)
            #update session values
            userFile['q2']['total'] = 1+userFile['q2']['total']
            userFile['q2']['current'] = patientID
            res.updateUserFile(username, userFile)
        else:
            flash(error)
            
    #returns a random list of IDs 
    sampleList = res.returnRandomSample()
    sampleNumber=len(sampleList)
    
    
    #query the number
    if userFile['q2']['total'] == 0:
        left = sampleNumber 
        patientID = sampleList[0]
        
    elif userFile['q2']['total'] == sampleNumber:
        #the user has reached the max sample number
        return redirect(url_for('index'))
    else:
        left = sampleNumber - userFile['q2']['total']
        patientID=userFile['q2']['current']
        #find the index of the actual value and select the next ID
        j = 0
        for i in sampleList:
            j+=1
            print(patientID)
            if i == patientID:
                break 
        patientID=sampleList[j]
        print(patientID)
    
    patient = res.loadSampleFile(patientID)
    patientDetails = patient['patient']['details']
    patientHealthConditions = patient['patient']['data']
    
    return render_template('eval/question2.html',patientid=patientID,sample=sample, left=left,
                           details=patientDetails,conditions=patientHealthConditions,
                           total=sampleNumber)

@bp.route('/question3', methods=('GET', 'POST'))
def question3():
    
    return render_template('eval/question3.html')