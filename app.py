from flask import Flask, render_template, request, redirect
from datetime import datetime
import pytz
import mysql.connector as conn
app = Flask(__name__)
IST = pytz.timezone('Asia/Kolkata')  # Set timezone to IST
@app.route('/', methods = ['GET','POST'])

def home():
    connection= conn.connect(host="mysql-sid-todo-flask.alwaysdata.net",
    user="404053",
    password="sidmysqlalwaysdata",
    database="sid-todo-flask_test")
    if connection.is_connected():
        print(timestamp)
        print("Connected")
    db_cursor = connection.cursor()
   
    # capturing form 
    if request.method == 'POST':
        task = request.form["task"]
        desc = request.form["desc"]
        timestamp = datetime.now(pytz.utc)
        
        db_cursor.execute("INSERT INTO `todo`(`Name`, `Description`,`Timstamp`) VALUES (%s,%s,%s)",(task,desc,timestamp))
        if connection.commit() is None:
            print(db_cursor.rowcount)

    db_cursor.execute("Select * from todo")
    rows = db_cursor.fetchall()
    # print(rows[0][1],"",rows[0][2])
    # print(rows[1][1],"",rows[1][2])
    # print(rows)

    return render_template("index.html",todo=rows)

@app.route('/delete/<int:id>')
def delete(id):
    connection= conn.connect(host="mysql-sid-todo-flask.alwaysdata.net",
    user="404053",
    password="sidmysqlalwaysdata",
    database="sid-todo-flask_test")
    if connection.is_connected():
        print("Connected")
    db_cursor = connection.cursor()
    db_cursor.execute("DELETE FROM `todo` WHERE Srno = %s",(id,))
    if connection.commit() is None:
        return redirect("/")
    else:
        return "Commit Failed"

@app.route('/edit/<int:id>', methods = ['GET','POST'])
def update(id):
    connection= conn.connect(host="mysql-sid-todo-flask.alwaysdata.net",
    user="404053",
    password="sidmysqlalwaysdata",
    database="sid-todo-flask_test")

    if connection.is_connected():
        print("Connected")
        db_cursor = connection.cursor()

        if request.method=='POST':
            task = request.form["task"]
            desc = request.form["desc"]
            db_cursor.execute("UPDATE `todo` SET `Name`= %s,`Description`= %s WHERE Srno = %s",(task,desc,id))
            if connection.commit() is None:
                return redirect("/")
            
        db_cursor.execute("SELECT `Srno`, `Name`, `Description` FROM `todo` WHERE Srno = %s",(id,))
        data = db_cursor.fetchall()
        return render_template("edit.html",data=data)


if __name__ == '__main__':
    app.run(debug= True)
   