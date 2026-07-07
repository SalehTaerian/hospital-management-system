import psycopg2
from app.config import Config

with open('app/database/schema.sql', 'r') as f:
    sql = f.read()

conn = psycopg2.connect(
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME
)
cursor = conn.cursor()
cursor.execute(sql)
conn.commit()
print("✅ Schema imported successfully!")
cursor.close()
conn.close()