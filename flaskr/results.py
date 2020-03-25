from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.mngmt.DataManagement import DataManagement

bp = Blueprint('resu', __name__)

@bp.route('/results', methods=('GET', 'POST'))
@bp.route('/res/results', methods=('GET', 'POST'))
@login_required
def resultsGEE():
    sample='1'
    #setting a number of samples the user will evaluate
    res = DataManagement()
    
    res.setDirectory(sample)
    
    sampleList = res.returnRandomSample()
    
    #results
    if request.method == 'POST':
        
        error=None
        answerValue = request.form.get('answer')
        
        
        if answerValue == "1":
            result = res.generateSampleQ2()
            print(result)
            if result:
                error = "Sample generated"
            else:
                error = "Problem generating sample"
        else:
            error = "Please select a Category from the list."
            
        if error is not None:
            flash(error)
    
    return render_template('res/results.html', resultList=sampleList)

@bp.route('/details', methods=('GET', 'POST'))
@bp.route('/res/details', methods=('GET', 'POST'))
@login_required
def details():
    sample='1'
    #setting a number of samples the user will evaluate
    res = DataManagement()
    
    patientID = request.args.get('patientid')
    res.setDirectory(sample)
    patient = res.loadSampleFile(patientID)

    patientID = patientID.replace(".json","")
    patientDetails = patient['patient']['details']
    
    patientRelevantInf = patient['patient']['completeData']
    patientDistinctDatapoints = res.getDistinctDatapoints(patient['patient']['completeData'])
        
    return render_template('res/details.html', patientid=patientID,sample=sample, distinctDatapoints=patientDistinctDatapoints,
                           title='Details', details=patientDetails,relevant=patientRelevantInf)
