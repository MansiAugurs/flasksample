import pyodbc

def get_db_connection():
    server = 'localhost' 
    database = 'newDB'  
    username = 'user1' 
    password = 'user1' 
    cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return cnxn
