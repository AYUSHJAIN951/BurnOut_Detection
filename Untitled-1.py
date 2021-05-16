def get_days(d0, d1):
    
    d0 = pd.to_datetime(d0)
    d1 = pd.to_datetime(d1)
    delta = d1 - d0
    return delta.days

from pymongo import MongoClient
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


client = MongoClient()
datas=[]
db = client.burnout
todos = db.database #Select the collection name
x=todos.find()
dic={}

for key,todo in enumerate(x):
    EmployeeID=todo['Employee_ID']
    Date_of_Joining=todo['Date_of_Joining']
    Gender=todo['Gender']
    Company_Type=todo["Company_Type"]
    WFH_Setup_Available=todo["WFH_Setup_Available"]
    Designation=todo["Designation"]
    Resource_Allocation=todo["Resource_Allocation"]
    Mental_Fatigue_Score=todo["Mental_Fatigue_Score"]
    Burn_Rate=todo["Burn_Rate"]
    new=[EmployeeID,Date_of_Joining,Gender,Company_Type,WFH_Setup_Available,Designation,Resource_Allocation,Mental_Fatigue_Score,Burn_Rate]
    dic.update({key:new})
    
data=pd.DataFrame.from_dict(
    dic,    
    orient="index",
    columns=["Employee_ID","Date_of_Joining","Gender", "Company_Type", "WFH_Setup_Available","Designation","Resource_Allocation","Mental_Fatigue_Score","Burn_Rate"],
    )
# print(data)
# data.info()
train_df=data
train_df.dropna(inplace=True)
# train_df.info()
# print(train_df)

dataset=[train_df]
for data in dataset:
    data['Date_of_Joining']= pd.to_datetime(data['Date_of_Joining'])
    data['Gender']=[1 if (Gender == 'Male') else 0 for Gender in data.Gender]
    data['Company_Type']=[1 if (Company=='Service') else 0 for Company in data['Company_Type']]
    data['WFH_Setup_Available']=[1 if (WFH=='Yes') else 0 for WFH in data['WFH_Setup_Available']]
    data['JobDuration'] = [get_days(d, '2009-2-1') for d in data['Date_of_Joining']]
    data['JobDurationMonth'] = (data['JobDuration']/30)

# print(train_df)
train_df=train_df.drop(["Employee_ID","Date_of_Joining","JobDurationMonth"],axis=1)
train_df.info()
# train_df.to_csv('traindataprocessed.csv',index=False)



y=train_df['Burn_Rate']
X=train_df.drop(['Burn_Rate'],axis=1)
# y,X
# train_set,test_set = train_test_split(train_df.drop(['Burn Rate'],axis=1),test_size=0.3 , random_state=50)

# X=train_set
# y=train_labels
x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=12340)
print(x_train)
x_train.info()
print(x_test)

x_test.info()
print(y_train)


# print(1)

from sklearn.linear_model import LinearRegression as lm
model1=lm().fit(x_train,y_train)
predictions=model1.predict(x_test)
import matplotlib.pyplot as plt
# plt.scatter(y_test,predictions)
# plt.xlabel('True values')
# plt.ylabel('Predictions')
# plt.show()
print(predictions)
print(model1.score(x_test,y_test))



from sklearn import metrics
print('Mean Absolute Error: ', metrics.mean_absolute_error(y_test,predictions))
print('Root Mean Squared Error', np.sqrt(metrics.mean_squared_error(y_test,predictions)))
print('R2 Score', metrics.r2_score(y_test,predictions))
