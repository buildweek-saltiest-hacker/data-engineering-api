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

comments_df = pd.read_csv("hacker-comments.csv")
hacker_df = pd.read_csv("hacker-table.csv")

comments = comments_df.to_dict("records")
hackers = hacker_df.to_dict("records")

list_of_comments = [(c["hacker_name"], c["hacker_comment"], c["comment_saltiness"], c["hacker_score"]) for c in comments]
list_of_hackers = [(h["rank"], h["name"], h["score"]) for h in hackers]

insert_comments = "INSERT INTO comment (author, comment, saltiness, score) VALUES %s"
execute_values(cursor, insert_comments, list_of_comments)

insert_hackers = "INSERT INTO hacker (rank, name, score) VALUES %s"
execute_values(cursor, insert_hackers, list_of_hackers)
connection.commit()

cursor.close()
connection.close()
