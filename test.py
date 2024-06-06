import secrets
import sqlite3
from sqlite3 import Error


def generate_token(size=4):
    return secrets.token_hex(size)


print(generate_token())


def connect_db(db_file):
    """เชื่อมต่อกับฐานข้อมูล SQLite"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite database: {db_file}")
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

con = connect_db("docs.db")

def fetch_data(conn,table,token):
    """ดึงข้อมูลจากตาราง"""
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} where token = '{token}' ")
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(f"Error fetching data: {e}")
        return None
    
def fetch_alldata(conn, table):
    """ดึงข้อมูลจากตาราง"""
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(f"Error fetching data: {e}")
        return None


# ดึงข้อมูลทั้งหมด
def test(token):
    rows = fetch_data(con,"pdf",token)
    filename = rows[0][1]
    print(filename)
    return filename



def update_data(conn,table, data, condition):
    """แก้ไขข้อมูลในตาราง"""
    try:
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        cur = conn.cursor()
        cur.execute(sql, tuple(data.values()))
        conn.commit()
        return cur.rowcount
    except Error as e:
        print(f"Error updating data: {e}")
        return None
    
def update_token(token):
    rows = fetch_data(con,"pdf",token)
    name = rows[0][1]
    newToken = generate_token()
    update_data(con,"pdf",{"token":newToken},f"name ='{name}'")
    
   

    
# def test3():
#     conn = connect_db("docs.db")
#     docs = conn.execute('SELECT * FROM pdf').fetchall()
#     print(docs)
#     for doc in docs:
#         print(doc[1])
# test3()