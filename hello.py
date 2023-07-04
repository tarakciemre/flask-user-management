from flask import Flask
from flask import request
import psycopg2
import json
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, Integer
from sqlalchemy import MetaData

# ORM
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session


app = Flask(__name__)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "myusertable"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    username: Mapped[str] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String)
    middlename: Mapped[str] = mapped_column(String)
    lastname: Mapped[str] = mapped_column(String)
    birthdate: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)


engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/flask_db", echo=True)

Base.metadata.create_all(engine)


def dict_to_json(arg):
    return json.dumps(arg, indent=4, sort_keys=True, default=str)


def insert_user(data):
    sess = Session(engine)
    temp_user = User(**data)
    sess.add(temp_user)
    sess.flush()         # applies the change in the active version of the database.
    sess.commit()        # saves the changes to the database and makes them persist.
    sess.close()


def update_user(user_id, data):
    session = Session(engine)
    temp = session.query(User).get(user_id)
    for (k, v) in data.items():
        setattr(temp, k, v)
    session.flush()
    session.commit()
    session.close()


def get_all_users():
    session = Session(engine)
    temp = session.query(User).all()
    print(str(temp))
    users_json = json.dumps(list(map(lambda a: a.as_dict(), temp)))
    session.flush()
    session.commit()
    session.close()
    return users_json


def delete_user(user_id):
    session = Session(engine)
    user_to_delete = session.query(User).get(user_id)
    session.delete(user_to_delete)
    session.flush()
    session.commit()
    session.close()


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
