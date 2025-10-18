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
