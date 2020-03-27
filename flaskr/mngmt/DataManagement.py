'''
Created on 21 Feb 2020

@author: acmt2
'''
import os, os.path
import json
import random
from fileinput import filename
import csv, shutil, time
from csv import writer

class DataManagement():
    directory = 0
    patientList = 0
    totalResult = 0
    resultsDirectory = 0
    
    def __repr__(self):
        #self.totalResult = self.getTotalExamples()
        return '<Results {}>'.format(self.body)
    
    def setDirectory(self, sample):
        self.resultsDirectory = os.getcwd()+ '/flaskr/users/'
        
        if sample == '1':
            self.sampleDirectory = os.getcwd()+ '/flaskr/sample/'
        elif sample == '2':
            self.sampleDirectory = os.getcwd()+ '/flaskr/sampleq2/'
        '''print(os.getcwd())
        print(self.resultsDirectory)'''
        
    def getTotalExamples(self):
        self.totalResult = len(self.patientList)
        return self.totalResult
    
    def returnTotalExamples (self):
        # load the list of patients ID in the directory
        self.patientList = [f for f in os.listdir(self.directory) if not f.startswith('.')] 
        self.totalResult = len(self.patientList)
        return self.patientList
    
    def returnRandomSample(self):
        randomSampleList = [f for f in os.listdir(self.sampleDirectory) if not f.startswith('.')] 
        return randomSampleList
    #Load any file from the specified directory
    def loadFile (self, fileName):
        #with open(self.directory+patientid+".json") as json_file:
        with open(self.directory+fileName) as json_file:
            obj = json.load(json_file)
        return obj
    #load only sample files
    def loadSampleFile (self, fileName):
        with open(self.sampleDirectory+fileName) as json_file:
            obj = json.load(json_file)
        return obj
    
    def loadUserFile (self, fileName):
        obj = None
        if os.path.isfile(self.resultsDirectory+fileName + ".json"):
            with open(self.resultsDirectory+fileName + ".json") as json_file:
                obj = json.load(json_file)
        return obj
    
    def verifyUser(self, username):
        usersList = [f for f in os.listdir(self.resultsDirectory) if not f.startswith('.')] 
        username = username + ".json"
        file =False
        for user in usersList:
            if user == username:
                file = True
                pass
        
        return file
    
    def generateUserID(self, flag, username):
        idcode = 1
        
        if flag:
            #the username already has an IDCODE
            userfile = self.loadUserFile(username)
            idcode = userfile[id]
        else:
            usersList = [f for f in os.listdir(self.resultsDirectory) if not f.startswith('.')] 
            usersCount = len(usersList)
        
            if usersCount > 0:
                idcode = usersCount+1
            
        return idcode
    
    def createUserFile(self, username):
        userid = self.generateUserID(False, username)
        content = {}
        content['id'] = userid
        content['username'] = username
        content['q1'] = {}
        content['q1']['total'] = 0
        content['q1']['current'] = 0
        content['q2'] = {}
        content['q2']['total'] = 0
        content['q2']['current'] = 0
        with open(self.resultsDirectory+username +".json", 'w') as outfile:
            json.dump(content,outfile)
    
    def updateUserFile(self, username, content):
        with open(self.resultsDirectory+username +".json", 'w') as outfile:
            json.dump(content,outfile)
            
    def createCSVresultsFile(self,name):
        with open(self.resultsDirectory+name+'.csv', mode='w') as csv_file:
            fieldnames = ['username', 'question', 'patientid','answer','value','order']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
            writer.writeheader()
            
    def appendRowsCSVresultsFile(self,name, dictRow):
        with open(self.resultsDirectory+name+'.csv', 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(dictRow)
            
    def obtainCategoryName(self, identifier):
        categories = self.getCategoriesDic()
        
        for i in categories:
            if i['id'] == identifier:
                return i['name']
            
    def getCategoriesDic(self):
        categories = [{'name':'Electric Wheelchair and wheelchair user', 'id': '01'},
                  {'name':'Mobility impaired person','id': '03'},
                  {'name':'Ashtma and breathing issues','id': '04'},
                  {'name':'Visually impaired person','id': '05'},
                  {'name':'Dyslexic and orientation disorders','id': '06'},
                  {'name':'Learning difficulty and autism','id': '07'},
                  {'name':'Mental Health problems','id': '08'},
                  {'name':'Dexterity problems','id': '09'}]
        return categories
    
            
    def getButtonLabel(self, cod):
        if cod == "1":
            return "Yes (recent)"
        elif cod == "2":
            return "Yes (chronic)"
        elif cod == "3":
            return "Yes (both)"
        elif cod == "4":
            return "No"
        elif cod == "5":
            return "I cannot say"
        
    def getDistinctDatapoints(self, dataPoints):
        #create a new list, already all the list objects are sorted by description
        #reason description and date
        newList = None
        newDataPoint= {}
        i=0
        for a in dataPoints:
            #con could be encounters, conditions, allergies, etc
            for con in a:
                for c in a[con]['results']['bindings']:
                    if newList is None:
                        newList =[]
                        newList.append(c)
                        i=0
                    else:
                        if newList[i]['reasonDescription']['value'] != c['reasonDescription']['value']:
                            newList.append(c)
                            i+=1
                        else:
                            try:
                                if newList[i]['description']['value'] != c['description']['value']:
                                    newList.append(c)
                                    i+=1
                            except KeyError:
                                pass
            
            newDataPoint[con]=newList
            newList=None
            
        return newDataPoint
        
    def verifyAdmin(self, userFile):
        try:
            if userFile['admin'] == 'YES':
                return True
            else:
                return False
        except:
            return False
        
    def generateSampleQ2(self):
        self.resultsDirectory = self.resultsDirectory+ 'resultsGSE.csv'
        result = False
        try:
            with open(self.resultsDirectory, newline='') as f:
                reader = csv.reader(f)
                samplelist = list(reader)
        
            for item in samplelist:
                assistance = item[1]
                idpatient = item[0]
                print(assistance)
                
                if assistance == '1' or assistance == '2' or assistance == '3':
                    
                    dir_origin = os.getcwd()+ '/flaskr/sample/' + idpatient + '.json'
                    dir_destin = os.getcwd()+ '/flaskr/sampleq2/'

                    # if item is a file, copy it
                    if os.path.isfile(dir_origin):
                        shutil.copy(dir_origin, dir_destin)
                        result = True
                    else:
                        result = False
            time.sleep(2)
        except Exception as e:
            print("EX: "+ str(e))
            result = False
        return result
    
    def getResultsQ1Sys(self):
        self.directory= self.resultsDirectory
        systemResults = self.loadFile("sampleSummary4Sys.json")
        
        return systemResults
    
    def getResultsQ1GSE(self):
        self.resultsDirectory = self.resultsDirectory+ 'resultsGSE.csv'
        try:
            with open(self.resultsDirectory, newline='') as f:
                reader = csv.reader(f)
                samplelist = list(reader)
        except Exception as e:
            print("EX: "+ str(e))
             
        return samplelist
        
    def getGSAnswer(self,identification):
        self.resultsDirectory = self.resultsDirectory+ 'resultsGSE.csv'
        result = []
        try:
            with open(self.resultsDirectory, newline='') as f:
                reader = csv.reader(f)
                samplelist = list(reader)
                
                for item in samplelist:
                    assistance = item[2]
                    note = item[5]
                    idpatient = item[0]
                    
                    if identification == idpatient:
                        result.append(assistance)
                        result.append(note)
                        break
        except Exception as e:
            print("EX: "+ str(e))
            
        return result