import psycopg2


# connect to database
conn = psycopg2.connect(host='xxxx', dbname='xxxx', user='xxxx',
                        password='xxxx', port=0000)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS workers(
    id INT PRIMARY KEY,
    name TEXT,
    age INT,
    height INT
);
""")

conn.commit()
cur.close()
conn.close()