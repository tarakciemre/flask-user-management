from flask import Flask
import psycopg2

app = Flask(__name__)

# [x] Create routes
# [ ] /login
# [ ] /logout
# [ ] /user/list
# [ ] /user/create
# [ ] /user/delete/{id}
# [ ] /user/update/{id}
# [ ] /onlineusers

def initializeDatabase():
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS userTable (
        id SERIAL,
        age INT,
        name VARCHAR(100)
        );'''
    )
    conn.commit()
    cur.close()
    conn.close()

initializeDatabase()

@app.route("/login")
def login():
    return "<p>Login page</p>"

@app.route("/logout")
def logout():
    return "<p>Logout page</p>"

@app.post("/user/create")
def userCreate():
    return "<p>Logout page</p>"

@app.get("/user/list")
def userList():
    return "<p>Logout page</p>"

@app.get("/user/delete/<id>")
def userDelete(id):
    return "<p>Logout page </p>" + str(id)

@app.post("/user/update")
def userUpdate():
    return "<p>Logout page</p>"

@app.get("/onlineusers")
def onlineUsers():
    return "<p>Online Users</p>"