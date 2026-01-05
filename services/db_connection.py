import pyodbc

def get_database_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=172.16.0.239;"
            "DATABASE=SFI_DWH;"
            "UID=usersfi;"
            "PWD=sfi.100;",
            timeout=5
        )
        print("[SYSTEM] CONNECTION SUCCESS.")
        return conn
    except pyodbc.Error as e:
        print(f"[ERROR] CONNECTION FAILED : {e}")
        return None

if __name__ == "__main__":
    get_database_connection()
