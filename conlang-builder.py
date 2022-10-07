from hashlib import new
from pyfiglet import Figlet
import sqlite3 #import module

#DEFINE FUNCTIONS

# def print_dict(database):  # temporary test function to print dictionary contents
#     conn = sqlite3.connect(database)
#     cursor = conn.cursor()
#     results = cursor.execute("SELECT * FROM dictionary ORDER BY natword ASC;")
#     list = results.fetchall()
#     cursor.close()
#     conn.close()
#     print(list)

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

# def edit_entry_by_nat(database, natword, newconword):
#     conn = sqlite3.connect(database)
#     cursor = conn.cursor()
#     cursor.execute("UPDATE dictionary SET conword=? WHERE natword=?", (newconword, natword))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return "Updated entry: now the word for " + natword + " is " + newconword

# def edit_entry_by_con(database, conword, newnatword):
#     conn = sqlite3.connect(database)
#     cursor = conn.cursor()
#     cursor.execute("UPDATE dictionary SET natword=? WHERE conword=?", (newnatword, conword))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return "Updated entry: now " + conword + " is the word for " + newnatword

def edit_entry(database, refNat, newNat, newCon):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    refCon = cursor.execute("SELECT conword FROM dictionary WHERE natword=?", (refNat,)).fetchone()[0]
    if refNat == newNat and refCon == newCon:
        return "There doesn't seem to be any change here!"
    elif refNat != newNat and refCon != newCon:
        return "You seem to be trying to add a completely new entry! You can only edit one part of the entry at a time."
    elif refNat != newNat:
        cursor.execute("UPDATE dictionary SET natword=? WHERE conword=?", (newNat, refCon))
    elif refCon != newCon:
        cursor.execute("UPDATE dictionary SET conword=? WHERE natword=?", (newCon, refNat))
    conn.commit()
    cursor.close()
    conn.close()
    return "Entry has been edited!"

def print_dictionary(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    results = cursor.execute("SELECT * FROM dictionary ORDER BY natword ASC").fetchall()
    cursor.close()
    conn.close()
    for row in results:
        print(row[0] + ": " + row[1])

# def export_to_csv(database):
    

def print_options():
    print("1) help: display this list of options")
    print("2) print: print your dictionary")
    print("3) new: add new entry")
    print("4) trans: look up a word's translation in either direction")
    print("5) edit: edit an existing entry")
    print("6) quit: exit the program")

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


#MAIN
f = Figlet(font='colossal')
print(f.renderText('C o n l a n g\nB u i l d e r'))
print("Welcome to Conlang Builder! Choose an option from the list below.\n")
print_options()

while(True):
    inp = input("\nWhat do you want to do?\n> ")
    print("")
    match inp:
        case "1" | "help":
            print_options()
        case "2" | "print": #print_dictionary
            print_dictionary(database)
        case "3" | "new": #define_new_word
            nat = input("Natlang word: ")
            con = input("Conlang word: ")
            define_new_word(database, nat, con)
        case "4" | "trans": #translate
            inputLang = input("What language are you translating from? (n for natlang, c for conlang)\n")
            query = input("What word do you want to look up?\n")
            if inputLang == "n":
                result = translate_nat_to_con(database, query)
            elif inputLang == "c":
                result = translate_con_to_nat(database, query)
            else:
                result = "Please choose n or c."
            print(result)
        case "5" | "edit": #edit_entry
            refNat = input("Which natword do you want to edit the entry for?\n")
            newNat = input("Natword: ")
            newCon = input("Conword: ")
            print(edit_entry(database, refNat, newNat, newCon))
        case "6" | "quit":
            break
        case _:
            print("That doesn't seem to be a valid option.")