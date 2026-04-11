import psycopg2
import csv
from config import load_config

def get_connection():
    params = load_config()
    return psycopg2.connect(**params)

def search_pattern():
    pattern = input("Pattern: ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    except Exception as e:
        print(e)

def upsert_user():
    name = input("Name: ")
    phone = input("Phone: ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
                conn.commit()
                print("Success")
    except Exception as e:
        print(e)

def bulk_insert_csv():
    filepath = input("CSV filepath: ")
    names = []
    phones = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                names.append(row[0])
                phones.append(row[1])
        
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL bulk_insert_contacts(%s, %s, NULL, NULL);", (names, phones))
                failed = cur.fetchone()
                conn.commit()
                if failed and (failed[0] or failed[1]):
                    print("Failed to insert:", failed[0], failed[1])
                else:
                    print("All CSV data inserted successfully")
    except Exception as e:
        print(e)

def get_paginated():
    limit = input("Limit: ")
    offset = input("Offset: ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    except Exception as e:
        print(e)

def delete_user():
    identifier = input("Name or Phone to delete: ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s);", (identifier,))
                conn.commit()
                print("Deleted")
    except Exception as e:
        print(e)

def main_menu():
    while True:
        print("\n1. Search Pattern")
        print("2. Upsert Contact")
        print("3. Bulk Insert CSV")
        print("4. Paginated Query")
        print("5. Delete Contact")
        print("0. Exit")
        choice = input("Choice: ")
        
        if choice == '1':
            search_pattern()
        elif choice == '2':
            upsert_user()
        elif choice == '3':
            bulk_insert_csv()
        elif choice == '4':
            get_paginated()
        elif choice == '5':
            delete_user()
        elif choice == '0':
            break

if __name__ == '__main__':
    main_menu()