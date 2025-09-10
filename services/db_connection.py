import pyodbc

def get_database_connection():
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=172.16.1.176\\MCOLUAT_INSTANCE;"
        "DATABASE=MOBILE_COLLECTION;"
        "UID=rahiel.hafizh;"
        "PWD=user.100;"
    )