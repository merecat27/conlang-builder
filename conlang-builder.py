import sqlite3  #import module

#Options:
#   - change language
#   - translate conlang to natlang
#   - translate natlang to conlang
#       - edit entry
#   - define a new word (natlang to conlang)
#   - display list

#First: select language (create and open new or open existing)
#language = input("Which language are you working on today?")
language = "kainatiy"
database = language + "-dictionary.db"
# Setup:
conn = sqlite3.connect(database)  #connect to db, create if none exist
cursor = conn.cursor()  #create cursor for db connection
cursor.execute("CREATE TABLE IF NOT EXISTS dictionary(natword, conword)")  #create the dictionary if none exists
conn.commit()
cursor.close()
conn.close()

#Next: what do you want to do?
