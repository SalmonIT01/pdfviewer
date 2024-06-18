import psycopg2
from psycopg2 import sql


def condb():
    return psycopg2.connect(
        host = 'pdf_db',
        database = 'pdfDATABASE',
        user = 'postgres',
        password = 'panu101',
        port = '5432')
     

def showdb(conn):
    cursor = conn.cursor()
    select_query = sql.SQL('SELECT * FROM {table}').format(table=sql.Identifier('pdf'))
    cursor.execute(select_query)
    records = cursor.fetchall()
    cursor.close()
    return records

def insert_record(conn, table, data):
    cursor = conn.cursor()
    columns = data.keys()
    values = [data[column] for column in columns]
    insert_query = sql.SQL(
        'INSERT INTO {table} ({fields}) VALUES ({values}) RETURNING id'
    ).format(
        table=sql.Identifier(table),
        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
        values=sql.SQL(', ').join(map(sql.Placeholder, columns))
    )
    cursor.execute(insert_query, data)
    conn.commit()
    record_id = cursor.fetchone()[0]
    cursor.close()
    return record_id

def update_record(conn, table, record_id, data):
    cursor = conn.cursor()
    set_query = sql.SQL(', ').join(
        [sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder(k)) for k in data.keys()]
    )
    update_query = sql.SQL(
        'UPDATE {table} SET {fields} WHERE id = {id}'
    ).format(
        table=sql.Identifier(table),
        fields=set_query,
        id=sql.Placeholder('id')
    )
    data['id'] = record_id
    cursor.execute(update_query, data)
    conn.commit()
    cursor.close()

def delete_record(conn, table, record_id):
    cursor = conn.cursor()
    delete_query = sql.SQL(
        'DELETE FROM {table} WHERE id = {id}'
    ).format(
        table=sql.Identifier(table),
        id=sql.Placeholder('id')
    )
    cursor.execute(delete_query, {'id': record_id})
    conn.commit()
    cursor.close()

def close_connection(conn):
    conn.close()
    
def get_token(conn,token):
    cursor = conn.cursor()
    select_query = f"SELECT name FROM pdf where token = '{token}'"
    cursor.execute(select_query)
    records = cursor.fetchall()
    cursor.close()
    
    return records[0][0] 

# conn = condb()
# print(showdb(conn))
# print(get_token(conn,'1w2'))

# def pee():
#     print('kuy pee')


def pp():
    print('no way action')





