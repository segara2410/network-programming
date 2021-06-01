import sqlite3, os, sys, time

start = time.time()

CREATE = False

if CREATE:
    try:
        os.remove("data.db")
    except:
        pass

db = sqlite3.connect("data.db")
cur = db.cursor()

if CREATE:
    counter = 0
    for ln in open("ExportSQL2.sql"):
        ln = ln.strip()
        cur.execute(ln)
        if counter % 1000 == 0:
            db.commit()
            sys.stdout.write(str(counter)+"..")
            sys.stdout.flush()
        counter += 1
    db.commit()

cur = db.cursor()
cur.execute("select count(*) from mockdata;")
print("\ncount(*) = ", cur.fetchone()[0])

cur = db.cursor()
rows=cur.execute("select FirstNameLastName, JobTitle, Company from mockdata where ID < 5")
for row in rows.fetchall():
    for i in range(len(row)):
        print(i, row[i])

db.close()

print("waktu: = ", time.time()-start)
