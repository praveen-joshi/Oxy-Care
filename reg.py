from flask import Flask,render_template,request
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="root",database="major")
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('regist.html')
@app.route('/',methods=['POST'])
def getval():
	nm=request.form["name"]
	em=request.form["email"]
	pd=request.form["password"]
	ct=request.form["city"]
	my=mydb.cursor()
	sqlform="insert into customer(name,email,pwd,city) values(%s,%s,%s,%s)"
    data=(nm,em,pd,ct)
    my.execute(sqlform,data)
    mydb.commit()
	
if __name__ == '__main__':
    app.run(debug=True)