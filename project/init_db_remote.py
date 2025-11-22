import mysql.connector
import os

# Load DB config from environment variables (fallback to hard‑coded values for safety)
DB_HOST = os.getenv('DB_HOST', 'metro.proxy.rlwy.net')
DB_PORT = int(os.getenv('DB_PORT', '34209'))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'kTiWlsuIcEWhufKIUEWvguIxhmruCiWe')
DB_NAME = os.getenv('DB_NAME', 'railway')

# Path to the schema file (relative to project root)
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'db', 'schema.sql')

def run_schema():
    # Read the whole schema file
    with open(SCHEMA_PATH, 'r') as f:
        sql_content = f.read()
    # Split on semicolons – mysql.connector can execute multi‑statement if we use execute many times
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=True,
    )
    cursor = conn.cursor()
    for stmt in statements:
        try:
            cursor.execute(stmt)
        except mysql.connector.Error as err:
            print(f"Error executing statement: {err.msg}")
    cursor.close()
    conn.close()
    print('Database schema applied successfully.')

if __name__ == '__main__':
    run_schema()
