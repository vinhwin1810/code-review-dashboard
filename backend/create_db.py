import pymysql

# Connect to the MySQL server
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="Counterstrike123"
)

# Create a cursor object to interact with the database
my_cursor = mydb.cursor()

# Create the database
my_cursor.execute("CREATE DATABASE MR_data")

# Show the list of databases
my_cursor.execute("SHOW DATABASES")

# Print the databases
for db in my_cursor:
    print(db)
