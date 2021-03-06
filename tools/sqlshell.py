import e32db



"""
import sys
sys.path.append('e:\\python') # to find sqlshell.py
from sqlshell import Q
import e32db
db = e32db.Dbms()
dbv = e32db.Db_view()
# might need db.create(...)
db.open(u'e:\\test.db')

## Create a new Captures Table
Q("DROP TABLE Captures")
Q("CREATE TABLE Captures (id COUNTER, site VARCHAR, date FLOAT, time FLOAT, ima INTEGER, xcoord INTEGER, ycoord INTEGER, position VARCHAR, family VARCHAR, subfamily VARCHAR, genus VARCHAR, species VARCHAR, sex VARCHAR, recapture VARCHAR, date_of_identification FLOAT, identified_by VARCHAR, comments LONG VARCHAR, picture_filename VARCHAR, audio_filename VARCHAR, specimen_code VARCHAR)",db, dbv)
Q("CREATE UNIQUE INDEX id_index ON Captures (id)",db,dbv)

## Create a new Traps Table
Q("DROP TABLE Traps")
Q("CREATE TABLE Traps (id COUNTER, site VARCHAR, date FLOAT, time FLOAT, ima INTEGER, xcoord INTEGER, ycoord INTEGER, position VARCHAR, date_of_first_baiting FLOAT, height FLOAT, temperature FLOAT, humidity FLOAT, wind_speed FLOAT, date_of_bait_prep FLOAT, date_of_bait_refill FLOAT, canopy_cover VARCHAR, collectors VARCHAR, comments LONG VARCHAR)",db, dbv)
Q("CREATE UNIQUE INDEX id_index ON Traps (id)",db,dbv)


############# YOU DON'T NEED TO RUN THIS ##################
## Altering a table (this is just an example and not needed...)
Q("ALTER TABLE Captures ADD picture_filename VARCHAR",db,dbv)
Q("ALTER TABLE Captures ADD audio_filename VARCHAR",db,dbv)
Q("ALTER TABLE Captures ADD specimen_code VARCHAR",db,dbv)


Q("SELECT * FROM Person", db, dbv)

>>> Q("CREATE TABLE person (id COUNTER, name VARCHAR)")
0 rows affected
>>> Q("INSERT INTO person(name) VALUES ('Korakot')")
1 rows affected
>>> Q("INSERT INTO person(name) VALUES ('morning_glory')")
1 rows affected
>>> Q("SELECT * from person")
|0|      Korakot|
|1|morning_glory|
"""

def Q(sql, db, dbv):
    if sql.upper().startswith('SELECT'):
        dbv.prepare(db, unicode(sql))
        dbv.first_line()
        rows = []
        maxlen = [0] * dbv.col_count()
        for i in range(dbv.count_line()):
            dbv.get_line()
            result = []
            for i in range(dbv.col_count()):
                try:
                    val = dbv.col(i+1)
                except:    # in case coltype 16
                    val = None
                result.append(val)
                maxlen[i] = max(maxlen[i], len(str(val)))
            rows.append(result)
            dbv.next_line()
        fmt = '|'+ '|'.join(['%%%ds' % n for n in maxlen]) + '|'
        for row in rows:
            print fmt % tuple(row) 
    else:
        n = db.execute(unicode(sql))
        print '%d rows affected' % n
