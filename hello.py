from flask import Flask
from flask import request
import psycopg2
import json
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, Integer
from sqlalchemy import MetaData

#ORM
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

app = Flask(__name__)

# This base object has a property called Base.metadata, and it takes care of the metadata management.
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "myusertable"

    username: Mapped[str] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String)
    middlename: Mapped[str] = mapped_column(String)
    lastname: Mapped[str] = mapped_column(String)
    birthdate: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/flask_db", echo=True)

# user_table = Table(
#     "myusertable",
#     metadata_obj,
#     Column("username", String, primary_key=True),
#     Column("firstname", String),
#     Column("middlename", String, nullable=True),
#     Column("lastname", String),
#     Column("birthdate", String),
#     Column("email", String),
#     Column("password", String)
# )

Base.metadata.create_all(engine)

# [x] Create routes
# [ ] /login
# [ ] /logout
# [ ] /user/list
# [ ] /user/create
# [ ] /user/delete/{id}
# [ ] /user/update/{id}
# [ ] /onlineusers

# TODO FOR JUNE 03
# DONE: Complete the database inserts and deletes
# TODO: Use SQL Alchemy instead of pure SQL
# TODO: Create a secure password saving with sha256 and salt

userProperties = [
    "username",
    "firstname",
    "middlename",
    "lastname",
    "birthdate",
    "email",
    "password"
]

def dict_to_json(arg):
    return json.dumps(arg, indent=4, sort_keys=True, default=str)

def initialize_database():
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS userTable (
        username VARCHAR NOT NULL UNIQUE,
        firstname VARCHAR NOT NULL,
        middlename VARCHAR,
        lastname VARCHAR NOT NULL,
        birthdate DATE,
        email VARCHAR NOT NULL,
        password VARCHAR NOT NULL
        );
        '''
    )
    conn.commit()
    cur.close()
    conn.close()


def insert_user(data):
    print(str(data))
    print("username: " + str(data["username"]))

    # parse the data
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute(
        '''
        INSERT INTO userTable (
        username,
        firstname,
        middlename,
        lastname,
        birthdate,
        email,
        password )
        VALUES
        (
        '''
        + ', '.join(
            map(
                lambda a: "'" + str(a) + "'",
                map(lambda a: data[a], userProperties)
            )

        ) +
        '''
        );
        '''
    )
    conn.commit()
    cur.close()
    conn.close()


def update_user(user_id, data):
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")
    cur = conn.cursor()
    print("DEBUG == " + str(data))
    cur.execute(
        '''
        UPDATE userTable
        SET 
        '''
        +
        ', '.join({"" + str(k) + " = \'" + str(v) + "\'" for (k, v) in data.items()})
        +
        '''
        WHERE username = \'''' + user_id + '''\'
        '''
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
        '''
        SELECT *
        FROM userTable
        '''
    )
    result = cur.fetchall()
    print(str(result))
    dict_result = list(map(lambda a: dict(zip(userProperties, a)), result))
    print(str(dict_result))
    print(dict_result)
    conn.commit()
    cur.close()
    conn.close()
    return dict_result


def delete_user(id):
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="1234",
                            host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute(
        '''
        DELETE 
        FROM userTable
        WHERE username = \'''' + id + '''\';
        '''
    )
    conn.commit()
    cur.close()
    conn.close()


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
    insert_user(data)
    return "<p>Logout page</p>"


@app.get("/user/list")
def user_list():
    users = get_all_users()
    users_json = dict_to_json(users)
    return str(users_json)


@app.get("/user/delete/<user_id>")
def user_delete(user_id):
    delete_user(user_id)
    return "<p>Logout page </p>" + str(user_id)


@app.post("/user/update/<user_id>")
def user_update(user_id):
    data = request.get_json()
    update_user(user_id, data)
    return "<p>Logout page</p>" + str(data)


@app.get("/onlineusers")
def online_users():
    return "<p>Online Users</p>"
