import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

df = pd.read_csv("data/bronze/news.csv")

print("Rows to insert:", len(df))

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO bronze_news (title, content, source, url, date, category)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row["title"],
        row["content"],
        row["source"],
        row["url"],
        row["date"],
        row["category"]
    ))

conn.commit()
cursor.close()
conn.close()

print("✅ Data inserted into Supabase")