# Create a singular connection to sqlite and db file to share with every other file
import sqlite3
con = sqlite3.connect("./project.sqlite")
cur = con.cursor()