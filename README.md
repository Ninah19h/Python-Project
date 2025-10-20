Environment setup

Clone the Repository
> git clone https://github.com/yourusername/crime-reporting-system.git
> cd crime-reporting-system

Set Up Virtual Environment
> python -m venv env

Activate on linux
> source env/bin/activate

Install Dependancies 
> pip install -r requirements.txt

Set Up PostgreSQL Database (for those without the table)
> CREATE DATABASE crime_reporting_db;

Configure Environment Variables
> Create a .env file at the project root
DB_HOST=localhost
DB_NAME=crime_reporting_db
DB_USER=postgres
DB_PASSWORD=Password
DB_PORT=5432

 Initialize Database Tables
 > python -c "from database.connection import init_pool, execute_schema; init_pool(); execute_schema()"

 To run the program
 > python main.py

PROJECT STRUCTURE 

crime-reporting-system/
│
├── database/
│   ├── connection.py      # Talks to PostgreSQL database
│   └── schema.sql         # Creates the 4 tables (citizens, officers, cases, case_updates)
│
├── operations/
│   ├── citizen_ops.py     # Add, view, update, delete citizens (Contains all the database functions)
│   ├── officer_ops.py     # Add, view, update, delete officers (Contains all the database functions)
│   ├── case_ops.py        # Add, view, filter, update cases (Contains all the database functions)
│   └── case_update_ops.py # Add, view case progress notes (Contains all the database functions)
│
├── ui/
│   └── menu.py            # What you see and interact with (menus, input forms)
│
├── main.py                # The file you run to start the system
├── requirements.txt       # List of Python packages needed
├── .env                   # Your database password (secret, not shared)
├── .gitignore            # Tells Git what NOT to upload
└── README.md             # Instructions and documentation

Check existing tables
> sudo -u postgres psql

Connect to db
> \c crime_reporting_db

Check for tables
> \dt

Check inside the tables
SELECT * FROM citizens;
SELECT * FROM officers;
SELECT * FROM case_updates;
SELECT * FROM cases;

Exit the db
> \q

Run the program 
> python main.py


Project Title
Crime Reporting & Tracking System

Languages & Tools
•	Python
•	PostgreSQL
•	psycopg2 (for connecting to the database)
Database Schema
Tables:
•	citizens – stores citizen info
•	officers – stores officer info
•	cases – stores crime reports
•	case updates – tracks progress or notes on cases
Relationships:
•	One citizen can report many cases
•	One officer can handle many cases
•	One case can have many updates
Core Features
•	Citizens can report crimes
•	Police can view and update cases
•	Filter cases by:
o	Status (Pending / Resolved)
o	Location
o	Type of crime
 Database Operations
•	Add, read, update, and delete records
•	Join queries to display citizen and officer details per case
•	Filter queries for reports by type, status, or location


User Interaction (CLI Interface)
•	The system runs in the command line (terminal)


SUMMARY
The Crime Reporting & Tracking System is a Python and PostgreSQL-based project that allows citizens to report crimes and police officers to manage and track them. It stores important details such as crime type, location, and status while keeping all case updates organized in the database. Using psycopg2 for database connection, the system performs CRUD operations and uses SQL queries to filter and display data. It maintains clear relationships between citizens, officers, and cases, aiming to make crime reporting more efficient, transparent, and easy to follow up.
