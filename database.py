import sqlite3


def create_connection():
    database = "database.db"

    connection = None

    try:
        connection = sqlite3.connect(database)
        print(f"Connected to SqlLite version {sqlite3.version}")
        return connection
    except sqlite3.Error as e:
        print(e)
        return None


def execute(connection, sql, data=tuple()):
    try:
        cursor = connection.cursor()
        cursor.execute(sql, data)
        connection.commit()
    except sqlite3.Error as e:
        print(e)

def create_person_table(connection):
    sql = """
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT
        )
    """
    execute(connection, sql)


def create_task_table(connection):
    sql = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            desc TEXT NOT NULL,
            personsId INTEGER,
            FOREIGN KEY (personsId) REFERENCES persons (id)
        )
    """
    execute(connection, sql)


def store_person(connection, name, email):
    sql = """
        INSERT INTO persons(name, email) VALUES (?, ?)
    """
    execute(connection, sql, (name, email))


def store_task(connection, desc, id):
    sql = """
        INSERT INTO tasks(desc, personsId) VALUES (?, ?)
    """
    execute(connection, sql, (desc, id))


def get_all_persons(connection):
    sql = """
        SELECT * FROM persons
    """
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for person in rows:
        print(person)


def main():
    connection = create_connection()
    if connection:
        create_person_table(connection)
        create_task_table(connection)

        #while True:
        #    name = input("Enter a name: ")
        #    email = input("Enter email address: ")
        #    store_person(connection, name, email)
        #    if input("Add more y/n? ").lower() == 'n':
        #        break

        #print("Enter tasks")
        #while True:
        #    desc = input("Enter a task description: ")
        #    id = int(input("Enter user id for this task: "))
        #    store_task(connection, desc, id)
        #    if input("Add more y/n? ").lower() == 'n':
        #        break

        get_all_persons(connection)
        connection.close()

if __name__ == '__main__':
    main()
