import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(override=True)

import mysql.connector

host = os.getenv('DB_HOST')
port = int(os.getenv('DB_PORT', 3306))
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

print(f"Connecting to: {user}@{host}:{port}/{database}")

try:
    conn = mysql.connector.connect(
        host=host, port=port, user=user,
        password=password, database=database,
        connect_timeout=5
    )
    print("OK - Connected!")
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Tables ({len(tables)}): {tables}")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")
