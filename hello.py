from flask import Flask

app = Flask(__name__)

# /login
# /logout
# /user/list
# /user/create
# /user/delete/{id}
# /user/update/{id}
# /onlineusers

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

@app.get("/user/delete")
def userDelete():
    return "<p>Logout page</p>"

@app.post("/user/update")
def userUpdate():
    return "<p>Logout page</p>"

@app.get("/onlineusers")
def onlineUsers():