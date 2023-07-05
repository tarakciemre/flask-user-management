from flask import Flask
from flask import request

# Utils
import json
import datetime

# Database Interaction
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, Integer, DateTime
from sqlalchemy import MetaData

# ORM
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

# Data serialization
import marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, SQLAlchemyAutoSchema

# Encryption
import bcrypt

app = Flask(__name__)


def encrypt_password(password, salt):
    return bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')


def generate_salt():
    return bcrypt.gensalt().decode('utf-8')


def pyobj_to_json(arg):
    return json.dumps(list(map(lambda a: a.as_dict(), arg)))


# Set up models
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "myusertable"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    username: Mapped[str] = mapped_column(String, primary_key=True)
    firstname: Mapped[str] = mapped_column(String)
    middlename: Mapped[str] = mapped_column(String)
    lastname: Mapped[str] = mapped_column(String)
    birthdate: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    salt: Mapped[str] = mapped_column(String)

class Log(Base):
    __tablename__ = "log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    endpoint: Mapped[str] = mapped_column(String)
    status: Mapped[int] = mapped_column(Integer)
    body: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# Marshmallow serializer schemas
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True  # Optional: deserialize to model instances


class LogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Log
        load_instance = True

log_schema = LogSchema()
user_schema = UserSchema()

# Set up engine
engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/flask_db", echo=True)

# Create tables if they do not already exist
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


# may not be needed
def dict_to_json(arg):
    return json.dumps(arg, indent=4, sort_keys=True, default=str)



def encrypt_and_salt_dictionary(arg):
    arg['salt'] = generate_salt()
    arg['password'] = encrypt_password(arg['password'], arg['salt'])
    return arg

# === Database interactions ===
def insert_user(data):
    # Function log params
    endpoint = "insert"

    # Encrypt
    encrypt_and_salt_dictionary(data)
    body = json.dumps(data)
    status = 0

    sess = Session(engine)

    print("==============================" + str(sess.query(User).get(data["username"])))
    if(sess.query(User).get(data["username"]) != None):
        status = 2 # username already taken
    ## Insert email checking logic
    else:
        try:
            user = user_schema.load(json.loads(body), session=sess)
            sess.add(user)
            sess.flush()         # applies the change in the active version of the database.
        except SQLAlchemyError as e:
            # error = str(e.__dict__['orig'])
            status = 1
            sess.rollback()

    temp_log = Log(status=status, endpoint=endpoint, body=body)
    sess.add(temp_log)
    sess.flush()
    sess.commit()
    sess.close()



def update_user(user_id, data):
    # Function log params

    sess = Session(engine)
    temp = sess.query(User).get(user_id)
    for (k, v) in data.items():
        setattr(temp, k, v)
    sess.flush()
    sess.commit()
    sess.close()


def get_all_users():
    # Function log params
    endpoint = "/users/list"

    sess = Session(engine)
    temp = sess.query(User).with_entities(
        User.username,
        User.firstname,
        User.middlename,
        User.lastname,
        User.birthdate,
        User.email)
    print(str(temp))
    users_json = pyobj_to_json(temp)
    sess.flush()
    sess.commit()
    sess.close()
    return users_json


def delete_user(user_id):
    sess = Session(engine)
    try:
        user_to_delete = sess.query(User).get(user_id)
        sess.delete(user_to_delete)
        sess.flush()
    except SQLAlchemyError as e:
        # set up error type
        sess.rollback()
    # Create log
    sess.commit()
    sess.close()


# === Routes ===
@app.route("/login")
def login():
    return "<p>Login page</p>"


@app.route("/logout")
def logout():
    return "<p>Logout page</p>"


@app.post("/user/insert")
def user_insert():
    data = request.get_json()
    insert_user(data)
    return "<p>Logout page</p>"


@app.get("/user/list")
def user_list():
    users = get_all_users()
    return str(users)


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
