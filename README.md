# Flask Web Application

A Flask JSON API with PostgreSQL database.

# Log
## 03.07.2023 - Day 1

### Goals 
- [x] the initial setup for the application

### Log
- install Flask
- set up PostgreSQL
- set up psycopg2 for database interactions
- set up Pycharm as Python IDE
- Set up the routes with pure SQL


## 04.07.2023 - Day 2

### Goals 
- [x] setup an ORM for database interactions

### Log
- install SQLAlchemy
- read the documentation tutorial for SQLAlchemy
- switch the database interaction to use SQLAlchemy
- setup the User table again

### Notes to myself
- MetaData object keeps the information regarding the database that can be used for table setup
- The main interaction point for ORM namespace is the Session object
- Session object takes control of the Engine and provides abstraction
- Setting up ORM tables and columns is simpler than Core, but Core can be better fine-tuned and can be used for performance-critical parts of the application

## 05.07.2023 - Day 3

### Goals 
- [ ] create and setup the Log table
- [x] implement hashed (with salt) password storage and login
- [ ] implement timestamps in PostgreSQL using timestamptz
- [ ] containerize 

### Log
- password hashing with salt using bcrypt library

### Notes to myself
- Creation of salt according to the OWASP specification	



