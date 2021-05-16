from flask import Flask , render_template,request,redirect,url_for
from sklearn.linear_model import LinearRegression as lm
import pickle
import pandas as pd
from flask_pymongo import PyMongo , pymongo
from bson.json_util import dumps
import os
from pymongo import MongoClient
UPLOAD_FOLDER = '/static/employeeimages'

def get_days(d0):
    d1='2009-2-1'
    d0 = pd.to_datetime(d0)
    d1 = pd.to_datetime(d1)
    delta = d1 - d0
    return delta.days

app = Flask(__name__)
app.secret_key = "secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_URI'] = "mongodb://localhost:27017/burnout"  #database location
app.secret_key = "escret"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
mongo = PyMongo(app) #databse intialised

# FOR CONNECTING TO MONGO ONLINE
# app.config['MONGO_DBNAME'] = 'database_name'
# app.config['MONGO_URI'] = 'mongodb://db_name:db_password@ds123619.mlab.com:23619/db_table_name'


client = MongoClient()

mongoii = os.getenv('MONGODB')
clientii = MongoClient(mongoii)

db = client.burnout
todos = db.database #Select the collection name




filename = 'burnout_model.sav'
model1=pickle.load(open(filename,'rb'))




@app.route('/',methods=["GET","POST"])
def index():
    if request.method=='POST':
        ID=request.values.get("ID")
        NAME=request.values.get("NAME")
        DESGN=request.values.get("DESGN")
        GENDER=request.form.get("GENDER")
        COM=request.values.get("COM")
        WFH=request.values.get("WFH")
        RA=request.values.get("RA")
        MFS=request.values.get("MFS")
        JD=request.values.get("JD")
        
        if(GENDER=="Male"):
            GENDER=int(1)
        else:
            GENDER=int(0)
        if(COM=="Service"):
            COM=int(1)
        else:
            COM=int(0)
        if(WFH=="Yes"):
            WFH=int(1)
        else:
            WFH=int(0)
        
        JDD=JD
        print(JD)
        JD = get_days(JD) 
        JDM = (JD/30)


        
        return redirect(url_for("action",ID=ID,NAME=NAME,DESGN=DESGN,GENDER=GENDER,COM=COM,WFH=WFH,RA=RA,MFS=MFS,JD=JD,JDM=JDM,JDD=JDD))
    return render_template('index.html')
    # ,ID=ID,NAME=NAME,DESGN=DESGN,GENDER=GENDER,COM=COM,WFH=WFH,RA=RA,MFS=MFS,JD=JD,JDM=JDM
@app.route('/<ID>/<NAME>/<DESGN>/<GENDER>/<COM>/<WFH>/<RA>/<MFS>/<JD>/<JDM>/<JDD>', methods=["GET","POST"])
def action(ID,NAME,DESGN,GENDER,COM,WFH,RA,MFS,JD,JDM,JDD):
    
    data=pd.DataFrame.from_dict(
       dict([("A", [GENDER,COM,WFH,DESGN,RA,MFS,JD,JDM])]),
       orient="index",
      columns=["Gender", "Company Type", "WFH Setup Available","Designation","Resource Allocation","Mental Fatigue Score","JobDuration","JobDurationMonth"],
    )
    predictions=model1.predict(data)
    preds=predictions[0]
    pred=int(predictions[0]*100)
    if(GENDER==1):
        GENDER="Male"
    else:
        GENDER="Female"
    if(COM==1):
        COM="Service"
    else:
        COM="Product"
    if(WFH==1):
        WFH="Yes"
    else:
        WFH="No"
    
    mongo.db.database.insert({'Employee_ID':ID,"Date_of_Joining":JDD,"Gender":GENDER,"Company_Type":COM,"WFH_Setup_Available":WFH,"Designation":DESGN,"Resource_Allocation":RA,"Menatal_Fatigue_Score":MFS,"Burn_Rate":preds})

    if(pred<50):
        tip="Remove the stressor \n You’re overwhelmed by your responsibilities at work, consider asking for help with tasks or delegating some of your responsibilities to others "
        exercise=""
    elif(pred<70 and pred>51):
        tip="Get more sleep Sleep is necessary for your emotional well-being.\n Aim to get the recommended eight hours of sleep each night. "
    else:
        tip="Medical treatment  Seeking professional help for mental exhaustion is important. A mental health professional, such as a therapist, can provide you with the tools you need to cope with stress and work through this difficult period"
    return  render_template('index.html',pred=pred,tip=tip) 



if __name__ == '__main__':
    app.run(debug=True)

# data=pd.DataFrame.from_dict(
#        dict([("A", [0, 1, 0,2.0,4.0,7.3,313,10.433333])]),
#        orient="index",
#       columns=["Gender", "Company Type", "WFH Setup Available","Designation","Resource Allocation","Mental Fatigue Score","JobDuration","JobDurationMonth"],
#     )