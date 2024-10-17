import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    
    # Create Client table
    conn.execute('''
    CREATE TABLE IF NOT EXISTS client (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        middle_name TEXT,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        account_type TEXT NOT NULL,
        password TEXT NOT NULL,
        phone INTEGER,
        address_line TEXT,
        address_line2 TEXT,
        city TEXT ,
        pincode INTEGER 
    );
    ''')
    
    # Create Advocate table
    conn.execute('''
    CREATE TABLE IF NOT EXISTS advocate (
        adv_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        middle_name TEXT,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        account_type TEXT NOT NULL,
        password TEXT NOT NULL,
        phone INTEGER,
        address_line TEXT ,
        address_line2 TEXT,
        city TEXT ,
        pincode INTEGER ,
        specialization TEXT 
    );
    ''')

    # Create Cases table with Foreign Keys
    conn.execute('''
    CREATE TABLE IF NOT EXISTS cases (
        case_id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_title TEXT NOT NULL,
        case_description TEXT,
        case_status TEXT NOT NULL,
        case_outcome TEXT NOT NULL,
        case_adv INTEGER,
        case_client INTEGER,
        FOREIGN KEY(case_adv) REFERENCES advocate(adv_id),
        FOREIGN KEY(case_client) REFERENCES client(client_id)
    );
    ''')

    conn.commit()
    conn.close()

init_db()
