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
- set up the routes with pure SQL


## 04.07.2023 - Day 2

### Goals 
- [x] setup an ORM for database interactions

### Log
- install SQLAlchemy
- read the documentation tutorial for SQLAlchemy
- switch the database interaction to use SQLAlchemy
- setup the User table again

### Notes to self
- MetaData object keeps the information regarding the database that can be used for table setup
- The main interaction point for ORM namespace is the Session object
- Session object takes control of the Engine and provides abstraction
- Setting up ORM tables and columns is simpler than Core, but Core can be better fine-tuned and can be used for performance-critical parts of the application

## 05.07.2023 - Day 3

### Goals 
- [x] create and setup the Log table
- [x] implement hashed (with salt) password storage and login
- [x] implement timestamps in PostgreSQL using timestamptz
- [ ] containerize >>>
	- will work on this later, i have not started deployment yet, so i will be adding more features before deploying the application

### Log
- password hashing with salt using **bcrypt** library
- SQLAlchemy ORM object to JSON serialization using **Marshmallow SQLAlchemy** library
- session management using **FlaskSession**
- add constraints for user creation and reading
- restrict functionality based on session

### Notes to self
- Creation of salt according to the OWASP specification	
- Use *Marshmallow* for *object serialization*
- Session management can be used to get a list of all online users
- The salts are stored along with the user information, and login process hashes password and salt to check against the password hash in the database



