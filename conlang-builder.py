import sqlite3 #import module

#DEFINE FUNCTIONS
def print_dict(database):  # temporary test function to print dictionary contents
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    results = cursor.execute("SELECT * FROM dictionary ORDER BY natword ASC;")
    list = results.fetchall()
    cursor.close()
    conn.close()
    print(list)

# def check_if_exists(database, word):  # possibly delete this func
#     conn = sqlite3.connect(database)
#     cursor = conn.cursor()
#     existsBool = cursor.execute("SELECT 1 FROM dictionary WHERE (natword=? OR conword=?)", (word,word)).fetchone()
#     cursor.close()
#     conn.close()
#     return existsBool

def check_for_natword(database, natword):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    result = cursor.execute("SELECT 1 FROM dictionary WHERE natword=?", (natword,)).fetchone()
    cursor.close()
    conn.close()
    if result:
        return True
    return False

def check_for_conword(database, conword):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    result = cursor.execute("SELECT 1 FROM dictionary WHERE conword=?", (conword,)).fetchone()
    cursor.close()
    conn.close()
    if result:
        return True
    return False

def define_new_word(database, natword, conword):
    if check_for_natword(database, natword):
        return "This word is already defined!"
    if check_for_conword(database, conword):
        return "This conword is already used!"
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dictionary VALUES (?,?)", (natword, conword))
    conn.commit()
    cursor.close()
    conn.close()
    return "New word pair successfully added."

def translate_nat_to_con(database, natword):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    conword = cursor.execute("SELECT conword FROM dictionary WHERE natword=?", (natword,)).fetchone()
    cursor.close()
    conn.close()
    if not conword:
        return "Word doesn't exist."
    return "".join(conword)

def translate_con_to_nat(database, conword):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    natword = cursor.execute("SELECT natword FROM dictionary WHERE conword=?", (conword,)).fetchone()
    cursor.close()
    conn.close()
    if not conword:
        return "Word doesn't exist."
    return "".join(conword)

def edit_entry_by_nat(database, natword, newconword):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("UPDATE dictionary SET conword=? WHERE natword=?", (newconword, natword))
    conn.commit()
    cursor.close()
    conn.close()
    return "Updated entry: now the word for " + natword + " is " + newconword

def edit_entry_by_con(database, conword, newnatword):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("UPDATE dictionary SET natword=? WHERE conword=?", (newnatword, conword))
    conn.commit()
    cursor.close()
    conn.close()
    return "Updated entry: now " + conword + " is the word for " + newnatword

def print_dictionary(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    results = cursor.execute("SELECT * FROM dictionary ORDER BY natword ASC").fetchall()
    cursor.close()
    conn.close()
    for row in results:
        print(row[0] + ": " + row[1])

#Options:
#   [ ] change language
#   [x] translate conlang to natlang
#   [x] translate natlang to conlang
#   [x] edit entry
#   [x] define a new word (natlang to conlang)
#   [x] display list

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


#TESTS
print(define_new_word(database, 'dog', 'kap'))
print(define_new_word(database, 'fire', 'şay'))
# print_dict(database)
print(check_for_natword(database, 'fire'))
# print_dict(database)
print(translate_nat_to_con(database, 'water'))
print(translate_con_to_nat(database, 'kap'))
print(edit_entry_by_nat(database, 'dog', 'köpek'))
# print_dict(database)
print(edit_entry_by_con(database, 'şay', 'fiyah'))
# print_dict(database)
print_dictionary(database)