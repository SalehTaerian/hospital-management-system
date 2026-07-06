from flask import Flask, render_template , request , redirect
import psycopg2
from contextlib import contextmanager

app = Flask(__name__)

dbConf = {
    "host": "127.0.0.1",
    "database": "hospital-management-system",
    "port": "5432",
    "user": "postgres",
    "password": "saleh1385",
}


@contextmanager
def connectToDb():
    conn = psycopg2.connect(**dbConf)
    try:
        yield conn
    finally:
        conn.close()
        



@app.route("/login",methods=["POST" , "GET"])
def loginPage():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn = connectToDb()
        cur = conn.cursor()
        cur.execute("select username ,password from patient where username = %s and password = %s, (username , password)")
        user = cur.fetchone()
        if user is None:
            msg = "نام کاربردی یا رمز عبور اشتباه است"
            return render_template("signin.html",msg=msg)
        else:
            render_template('index.html')
            
    else:       
        return render_template("signin.html")


@app.route("/signup")
def signupPage(request):
    return render_template("signup.html")


@app.route("/home")
def homePage():
    return render_template("index.html")


app.run(debug=True)
