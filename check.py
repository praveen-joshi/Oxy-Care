import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="root",database="major")
my=mydb.cursor()
sqlform="insert into customer(name,email,pwd,city) values(%s,%s,%s,%s)"
nm,em,pd,ct='Amit Kumar','ak@gmail.com','123456','shrinagar'
data=(nm,em,pd,ct)
my.execute(sqlform,data)
print("done")
mydb.commit()