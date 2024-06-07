import secrets
import sqlite3
from sqlite3 import Error


def generate_token(size=4):
    return secrets.token_hex(size)

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
    
import base64

def pdf_to_base64(name):
    
    pdf_path = f"E:/gradProject/pdfjs-4.3.136-dist (1)/pdfjs-4.3.136-dist/static/document/{name}.pdf"
    # เปิดไฟล์ PDF ในโหมดอ่านแบบไบนารี
    with open(pdf_path, "rb") as pdf_file:
        # อ่านข้อมูลในไฟล์ PDF
        pdf_data = pdf_file.read()
        # เข้ารหัสข้อมูลเป็น base64
        base64_encoded_data = base64.b64encode(pdf_data)
        # แปลงข้อมูล base64 จาก bytes เป็น string
        base64_string = base64_encoded_data.decode('utf-8')
    return base64_string   
print(test('00f80e37'))
    
