from flask import Flask, render_template, request
import sqlite3 as sql
import os
app = Flask(__name__)

import sqlite3

conn = sqlite3.connect('Quiz1Stu.db')
# print("Opened database successfully")

# conn.execute('CREATE TABLE SchoolRecHarsh (ID VARCHAR,Days VARCHAR,Start VARCHAR,End VARCHAR,Approval VARCHAR,Max VARCHAR,Current VARCHAR,Seats VARCHAR,Wait VARCHAR,Instructor VARCHAR,Course VARCHAR,Section VARCHAR)')
# print("Table created successfully")
# conn.close()
import csv
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, '/')
    print('target')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):        
        filename = file.filename        
        with open('classes.csv') as csvfile:
              readCSV = csv.reader(csvfile, delimiter=',')
              for row in readCSV:
                ID = row[0]
                Days =row[1]
                Start =row[2]
                End =row[3]
                Approval =row[4]
                Approval =row[5]
                Max =row[6]
                Current =row[7]
                Seats =row[8]
                Wait =row[9]
                Instructor =row[10]
                Course =row[11]
                Section =row[12]
                con = sql.connect("Quiz1Stu.db")
                cur = con.cursor()
                cur.execute("INSERT INTO SchoolRecHarsh (ID,Days,Start,End,Approval,Max,Current,Seats,Wait,Instructor,Course,Section) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(ID,Days,Start,End,Approval,Max,Current,Seats,Wait,Instructor,Course,Section))
                con.commit()
        return render_template('home.html')

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

@app.route('/Instructors', methods=['POST'])
def Instructors():
    Course= request.form['Course']
    Days= request.form['Days']  
    con = sql.connect("Quiz1Stu.db") 
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT Instructor FROM SchoolRecHarsh where Course like \'%'+Course+'%\' AND Days like \'%'+Days+'%\';') 
    # cur.execute('SELECT Instructor FROM SchoolRecHarsh where Course like \'%'+Course+'%\';')
    rows = cur.fetchall() 
    # return vehicleName
    return render_template('list.html', rows=rows)

if __name__ == '__main__':
   app.run(debug = True)