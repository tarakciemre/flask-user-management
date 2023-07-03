from flask import Flask
from flask import request
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

# TODO FOR JUNE 03
# TODO: Complete the database inserts and deletes
# TODO: Create a secure password saving with sha256 and salt


def initialize_database():
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


def get_all_users():
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute(
        '''SELECT name
        FROM usertable'''
    )
    result = cur.fetchall()
    print(result)
    conn.commit()
    cur.close()
    conn.close()
    return result


initialize_database()


@app.route("/login")
def login():
    return "<p>Login page</p>"


@app.route("/logout")
def logout():
    return "<p>Logout page</p>"


@app.post("/user/create")
def user_create():
    data = request.get_json()
    return "<p>Logout page</p>"


@app.get("/user/list")
def user_list():
    users = get_all_users()
    return "<p>Logout page</p>" + str(users)


@app.get("/user/delete/<user_id>")
def user_delete(user_id):
    return "<p>Logout page </p>" + str(user_id)


@app.post("/user/update")
def user_update():
    data = request.get_json()
    return "<p>Logout page</p>" + str(data)


@app.get("/onlineusers")
def online_users():
    return "<p>Online Users</p>"
