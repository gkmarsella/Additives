import psycopg2
import psycopg2.extras

def connect():
    c = psycopg2.connect("dbname=fadditives")
    return c


def search_food(brand, name, ingredients):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO snacks (brand, name, ingredients) VALUES (%s, %s, %s)", (brand, name, ingredients))
    conn.commit()
    cur.close()
    conn.close()