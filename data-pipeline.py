"""
API for the Salty Hacker Build Week Project

API Developers:
Iuliia Stanina
Robert Sharp
"""
import pandas as pd
import os
import psycopg2
from psycopg2.extras import DictCursor, execute_values

from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
cursor = connection.cursor(cursor_factory=DictCursor)

my_df = pd.read_csv("./hack-comments.csv")
records = my_df.to_dict("records")
list_of_tuples = [(r["hacker_name"], r["hacker_comment"], r["comment_saltiness"], r["hacker_score"]) for r in records]


insertion_query = "INSERT INTO comment (author, comment, saltiness, score) VALUES %s"
execute_values(cursor, insertion_query, list_of_tuples)
connection.commit()

cursor.close()
connection.close()