import psycopg2


# connect to database
conn = psycopg2.connect(host='xxxx', dbname='xxxx', user='xxxx',
                        password='xxxx', port=0000)

cur = conn.cursor()

cur.execute("""DROP TABLE IF EXISTS workers;""")

conn.commit()
cur.close()
conn.close()