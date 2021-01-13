from flask import Flask,render_template,request,session,logging,url_for,redirect
from flask_mysqldb import MySQL,MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
import mysql.connector
import pickle

mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="major")
app = Flask(__name__)
my=mydb.cursor()
app.secret_key="hello"
#engine=create_engine("mysql+://root:root@localhost/major")
#db=scoped_session(sessionmaker(bind=engine))

#app.config['MYSQL_HOST']="localhost"
#app.config['MYSQL_USER']="root"
#app.config['MYSQL_PASSWORD']="root"
#app.config['MYSQL_DB']="major"
#app.config['MYSQL_CURSORCLASS']="DictCursor"
#mq=MySQL(app)
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/regist')
def regist():
	#name=request.form["ex"]
	return render_template('regist.html')

@app.route('/ps',methods=['POST'])
def ps():
	nm=request.form.get("Username")
	em=request.form.get("email")
	pd=request.form.get("password")
	ct=request.form.get("city")
	#my=mydb.cursor()
	sqlform="insert into customer(name,email,pwd,city) values(%s,%s,%s,%s)"
	data=(nm,em,pd,ct)
	my.execute(sqlform,data)
	mydb.commit()
	return render_template('login.html')

@app.route('/adservice',methods=['GET','POST'])
def adservice():
	us=request.form["us"]
	pd=request.form["pd"]
	if us=="admin" and pd=="add123":
		session['us']=us
		return render_template('adservice.html',us=session['us'])
	else:
		return render_template('admin.html')   	

@app.route('/login')
def login():
	#name=request.form["ex"]
	if "em" in session:
		session.pop("em",None)
	return render_template('login.html')


mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="major")
my=mydb.cursor()
@app.route('/uservice',methods=['GET','POST'])
def uservice():
	#name=request.form["ex"]
	#em=request.form.get("email")
	#pd=request.form.get("pd")
	mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="major")
	my=mydb.cursor()
	if request.method=='POST':
		login=request.form
		em=login['em']
		pd=login['pd']
		my.execute("select * from customer where email='"+em+"' and pwd='"+pd+"' ")
		r=my.fetchall()
		count=my.rowcount
		if count==1:
			session['em']=em
			return render_template('uservice.html',em=session['em'])
		else:
			return render_template('login.html')
	else:
		return render_template('login.html')		
	mydb.commit()
	my.close()

@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/EV')
def EV():
	return render_template('EV.html',em=session['em'])
			
@app.route('/services')
def services():
	#name=request.form["ex"]
	return render_template('services.html')


@app.route('/yield',methods=['GET','POST'])
def yieldpredic():
	if(request.method=='GET'):
		return render_template('yield.html',em=session['em'])

	import numpy as np
	import matplotlib.pyplot as plt
	import pandas as pd
	from sklearn.ensemble import RandomForestRegressor
	val=request.form
	pro=int(val['pro'])
	area=int(val['Area'])
	Season=val['Season']
	District=val['District']
	Crop=val['Crop']
	render_template('login.html')

	print("loading Library complete")


	# dataset = pd.read_csv('CropData.csv')
	# dataset.dropna(inplace=True)      

	# y = dataset.iloc[:, -1].values
	# dataset=dataset.drop(columns=['Production'])

	# dataset=pd.get_dummies(dataset, drop_first=True)
	# X = dataset.iloc[:, :].values

	# print("Data Set is ready to use")


	# #fitting using random forest

	# regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
	# regressor.fit(X, y)

	# #dumping regressor object in a file named model
	# with open('datafile.txt', 'wb') as fh:
   	# 	pickle.dump(regressor, fh) 

	pickle_data = open("datafile.txt", 'rb')
	regressor = pickle.load(pickle_data)


	print("your model is ready")

	#predicting
	print("let us predict")
	dataset = pd.read_csv('CropData.csv')     

	dataset=dataset.drop(columns=['Production'])
	dataset.dropna(inplace=True) 

	area=int(val['Area'])
	Season=val['Season']
	District=val['District']
	Crop=val['Crop']
	render_template('login.html')


	user_data = pd.DataFrame([[area,Season,Crop,District]],columns=['Area', 'Season','Crop','District_Name'])
	final_data=pd.concat([user_data, dataset])

	final_data=pd.get_dummies(final_data, drop_first=True)
	final_data_with_dummy_var= final_data.iloc[:, :].values


	result=int(regressor.predict( [ final_data_with_dummy_var[0,:].reshape( len(final_data_with_dummy_var[0]) )  ]))
	print("final result is ready"+str(result))

    #pro=request.form.get(pro)
	result=int(result)
	return redirect(url_for('yieldresult',result=result,pro=pro))


@app.route('/yieldresult')
def yieldresult():
	result=int(request.args['result'])
	pro=request.args['pro']
	return render_template('yieldresult.html',result=result,em=session['em'],pro=pro)

@app.route('/species',methods=['GET','POST'])
def speciesreconize():
	if(request.method=='GET'):
		return render_template('species.html',em=session['em'])

	import numpy as np
	import matplotlib.pyplot as plt
	import pandas as pd
	import math 

	val=request.form
	Temperature=float(val['Temperature'])
	ph=float(val['ph'])
	phosphorus=float(val['phosphorus'])
	EC=float(val['EC'])
	shootdw=float(val['shootdw'])
	EC_log=math.log(EC,10)
	phosphorus_log=math.log(phosphorus,10)
	Soil_type=float(val['Soil_type'])

	State=val['State']
	District=val['District']

	user_data=[Temperature,ph,EC,phosphorus,Soil_type,EC_log,phosphorus_log,shootdw]

	print("loading Library complete")

	# #Training Data
	# dataset = pd.read_csv('mdata.csv')
	# X = dataset.iloc[:, :-1].values
	# y = dataset.iloc[:, -1].values

	# from catboost import CatBoostClassifier
	# classifier = CatBoostClassifier()
	# classifier.fit(X, y)
	# #dumping code to save time
	# #dumping classifier object in a file named species_dump
	# with open('species_dump.txt', 'wb') as fh:
   	# 	pickle.dump(classifier, fh) 

	pickle_data = open("species_dump.txt", 'rb')
	classifier = pickle.load(pickle_data)



	specie_pred=classifier.predict(user_data)
	#because result is a list till now
	specie_pred=specie_pred[0]
	
	species_list=['cabbage', 'carrot', 'cucumber', 'lettuce', 'oat', 'onion', 'ryegrass', 'tomato']
	result=species_list[specie_pred-1]

	return redirect(url_for('speciesresult',result=result,State=State,District=District,em=session['em']))


@app.route('/speciesresult')
def speciesresult():
	result=request.args['result']
	State=request.args['State']
	District=request.args['District']

	import numpy as np
	import pandas as pd
	dataset = pd.read_csv('crop.csv')
	X=dataset.iloc[:,:]

	#find only dataset containing our state and district correspondingly
	X=X[ (X.values==State)]
	X=X[ (X.values==District)]

	#for storing in list
	ls=[]
	common_speices=""
	for var in range(X.shape[0]):
		common_speices+=str(X.iloc[var]['commodity']+", ")
		ls.append(X.iloc[var]['commodity'])

	print(common_speices)
	
	return render_template('speciesresult.html',result=result,common_speices=common_speices,em=session['em'])


	

@app.route('/logout')
def logout():
	#name=request.form["ex"]
	session.pop("em",None)
	return redirect(url_for('login'))


@app.route('/Envirob',methods=['POST'])
def Envirob():
	nm=request.form.get("climate")
	em=request.form.get("size")
	tr=request.form.get("Trees")
	res=int(em)*9
	res=res//150
	res=res-int(tr)
	if nm=='Tropical':
		return render_template('tropical.html',no=res,em=session['em'])
	if nm=='Temperate':
		return render_template('temperate.html',no=res,em=session['em'])
	if nm=='Continental':
		return render_template('continental.html',no=res,em=session['em'])		
      
if __name__ == '__main__':
    app.run(debug=True)