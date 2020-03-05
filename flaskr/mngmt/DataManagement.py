'''
Created on 21 Feb 2020

@author: acmt2
'''
import os, os.path
import json
import random
from fileinput import filename
import csv   
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
        print(self.resultsDirectory)
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
    
    def loadFile (self, fileName):
        #with open(self.directory+patientid+".json") as json_file:
        with open(self.directory+fileName) as json_file:
            obj = json.load(json_file)
        return obj
    
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
            fieldnames = ['username', 'question', 'patientid','answer','value']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
            writer.writeheader()
            
    def appendRowsCSVresultsFile(self,name, dictRow):
        with open(self.resultsDirectory+name+'.csv', 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(dictRow)
            
    def obtainCategoryName(self, identifier):
        categories = [{'name':'Electric Wheelchair and wheelchair user', 'id': '01'},
                  {'name':'Mobility impaired person','id': '03'},
                  {'name':'Ashtma and breathing issues','id': '04'},
                  {'name':'Visually impaired person','id': '05'},
                  {'name':'Dyslexic and orientation disorders','id': '06'},
                  {'name':'Learning difficulty and autism','id': '07'},
                  {'name':'Mental Health problems','id': '08'},
                  {'name':'Dexterity problems','id': '09'}]
        
        for i in categories:
            if i['id'] == identifier:
                return i['name']
            
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
                print(con)
                for c in a[con]['results']['bindings']:
                    if newList is None:
                        newList =[]
                        newList.append(c)
                        i=0
                    else:
                        print(c)
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
            
        print(newDataPoint)
            
        return newDataPoint
        