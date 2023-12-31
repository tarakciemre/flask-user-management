from flask import Flask
from flask import request
from flask import session

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
from sqlalchemy import ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

# Data serialization
import marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, SQLAlchemyAutoSchema

# Encryption
import bcrypt

# Session
from flask_session import Session as FlaskSession

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
FlaskSession(app)


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
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    salt: Mapped[str] = mapped_column(String)


class Log(Base):
    __tablename__ = "log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    endpoint: Mapped[str] = mapped_column(String)
    status: Mapped[int] = mapped_column(Integer)
    body: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Online(Base):
    __tablename__ = "online"

    username: Mapped[User] = mapped_column(ForeignKey("myusertable"), primary_key=True)
    ipaddress: Mapped[str] = mapped_column(String)
    logindatetime: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


# Marshmallow serializer schemas
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True  # Optional: deserialize to model instances


class LogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Log
        load_instance = True


class OnlineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Online
        load_instance = True


log_schema = LogSchema()
user_schema = UserSchema()
online_schema = OnlineSchema()

# Set up engine
engine = create_engine("postgresql+psycopg2://postgres:1234@postgres:5432/flask_db", echo=True)

# Create tables if they do not already exist
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


# may not be needed
def dict_to_json(arg):
    return json.dumps(arg, indent=4, sort_keys=True, default=str)


def encrypt_and_salt_dictionary(arg):
    arg['salt'] = generate_salt()
    arg['password'] = encrypt_password(arg['password'], arg['salt'])


# ==== DATABASE INTERACTIONS ========
def insert_user(data):
    # Function log params
    endpoint = "insert"

    # Encrypt
    encrypt_and_salt_dictionary(data)
    status = 0

    sess = Session(engine)
    if sess.query(User).get(data["username"]) != None:
        status = 2              # username already taken
    elif len(sess.execute(select(User).where(User.email == data["email"])).all()) != 0:
        status = 3              # email taken
    else:           # uniqueness checks are successful
        try:
            user = User(**data)
            sess.add(user)
            sess.flush()         # applies the change in the active version of the database.
        except SQLAlchemyError as e:
            # error = str(e.__dict__['orig'])
            status = 1
            sess.rollback()
    temp_log = Log(status=status, endpoint=endpoint, body=json.dumps(data))
    sess.add(temp_log)
    sess.flush()
    sess.commit()
    sess.close()
    return status


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
    temp = sess.query(User).all()
    tmp = UserSchema(many=True).dumps(temp)
    sess.flush()
    sess.commit()
    sess.close()
    return tmp


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


def login(data):
    sess = Session(engine)
    if sess.query(User).get(data["username"]) == None:
        sess.close()
        return 10
    user = sess.query(User).get(data["username"])
    if user.password != encrypt_password(data["password"], user.salt):
        sess.close()
        return 11
    try:
        online = Online(username=data["username"], ipaddress=data["ipaddress"])
        sess.add(online)
        sess.flush()  # applies the change in the active version of the database.
        sess.commit()
    except SQLAlchemyError as e:
        sess.rollback()
    sess.close()
    return 0


def get_online_users():
    print("====>>> GET_ONLINE_USERS LOG ======<<<<<")
    sess = Session(engine)
    temp = sess.query(Online).all()
    print("temp: " + str(temp))
    tmp = OnlineSchema(many=True).dumps(temp)
    print("temp: " + str(tmp))
    sess.flush()
    sess.commit()
    sess.close()
    print("====>>> GET_ONLINE_USERS END ======<<<<<")
    return tmp


# === Routes ===
@app.post("/login")
def login_route():
    data = request.get_json()
    result = login(data)
    # if session.get("name") is not None:
    #     return "Already logged in"
    if result == 10:
        return "User does not exist"
    if result == 11:
        return "Wrong password"
    if result == 0:
        return "Login successful!"
        session["name"] = "Emre"


@app.route("/logout")
def logout():
    session.pop("name")
    return "Logged out"


@app.post("/user/insert")
def user_insert():
    # if not session.get("name"):
    #     return "You got no session"
    data = request.get_json()
    status = insert_user(data)
    if status == 0:
        return "Success!"
    if status == 1:
        return "Database error."
    if status == 2:
        return "User " + data["username"] + " already exists."
    if status == 3:
        return "Email " + data["email"] + " is already taken."


@app.get("/user/list")
def user_list():
    # if session.get("name") is None:
    #     return "You got no session"
    users = get_all_users()
    return str(users)
    # return "Dummy user list"


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
    users = get_online_users()
    return users
