import e32
import e32db
import orm
import md5

# This is the ORM to the table 'Traps'
class Traps(orm.Mapper):
    class mapping:
        site = orm.column(orm.String)
        date = orm.column(orm.Float) # try this with TIMESTAMP later?
        time = orm.column(orm.Float) # try this with TIMESTAMP later?
        ima = orm.column(orm.Integer)
        xcoord = orm.column(orm.Integer)
        ycoord = orm.column(orm.Integer)
        position = orm.column(orm.String)
        date_of_first_baiting = orm.column(orm.Float)
        height = orm.column(orm.Float)
        temperature = orm.column(orm.Float)
        humidity = orm.column(orm.Float)
        wind_speed = orm.column(orm.Float)
        date_of_bait_prep = orm.column(orm.Float)
        date_of_bait_refill = orm.column(orm.Float)
        canopy_cover = orm.column(orm.String)
        collectors = orm.column(orm.String)
        comments = orm.column(orm.String)
        barcode = orm.column(orm.String)
    def create_table(cls, db):
        q = u'CREATE TABLE ' + cls.__name__ + ' '
        q += '(id COUNTER,'
        q += 'site VARCHAR,'
        q += 'date FLOAT,'
        q += 'time FLOAT,'
        q += 'ima INTEGER,'
        q += 'xcoord INTEGER,'
        q += 'ycoord INTEGER,'
        q += 'position VARCHAR,'
        q += 'date_of_first_baiting FLOAT,'
        q += 'height FLOAT,'
        q += 'temperature FLOAT,'
        q += 'humidity FLOAT,'
        q += 'wind_speed FLOAT,'
        q += 'date_of_bait_prep FLOAT,'
        q += 'date_of_bait_refill FLOAT,'
        q += 'canopy_cover VARCHAR,'
        q += 'collectors VARCHAR,'
        q += 'comments LONG VARCHAR,'
        q += 'barcode VARCHAR)'
        db.execute(q)
        q = u'CREATE UNIQUE INDEX id_index ON '
        q += cls.__name__ + ' (id)'
        db.execute(q)
    create_table = classmethod(create_table)
    def drop_table(cls, db):
        q = u'DROP TABLE ' + cls.__name__
        db.execute(q)
    drop_table = classmethod(drop_table)

# This is the ORM to the table 'Captures'
class Captures(orm.Mapper):
    class mapping:
        site = orm.column(orm.String)
        date = orm.column(orm.Float) # try this with TIMESTAMP later?
        time = orm.column(orm.Float) # try this with TIMESTAMP later?
        ima = orm.column(orm.Integer)
        xcoord = orm.column(orm.Integer)
        ycoord = orm.column(orm.Integer)
        position = orm.column(orm.String)
        specimen_code = orm.column(orm.String)
        family = orm.column(orm.String)
        subfamily = orm.column(orm.String)
        genus = orm.column(orm.String)
        species = orm.column(orm.String)
        sex = orm.column(orm.String)
        recapture = orm.column(orm.String)
        date_of_identification = orm.column(orm.Float)
        identified_by = orm.column(orm.String)
        comments = orm.column(orm.String)
        picture_filename = orm.column(orm.String)
        audio_filename = orm.column(orm.String)
        visit_id = orm.column(orm.Integer)
    def create_table(cls, db):
        q = u'CREATE TABLE ' + cls.__name__ + ' '
        q += '(id COUNTER,'
        q += 'site VARCHAR,'
        q += 'date FLOAT,'
        q += 'time FLOAT,'
        q += 'ima INTEGER,'
        q += 'xcoord INTEGER,'
        q += 'ycoord INTEGER,'
        q += 'position VARCHAR,'
        q += 'specimen_code VARCHAR,'
        q += 'family VARCHAR,'
        q += 'subfamily VARCHAR,'
        q += 'genus VARCHAR,'
        q += 'species VARCHAR,'
        q += 'sex VARCHAR,'
        q += 'recapture VARCHAR,'
        q += 'date_of_identification FLOAT,'
        q += 'identified_by VARCHAR,'
        q += 'comments LONG VARCHAR,'
        q += 'picture_filename VARCHAR,'
        q += 'audio_filename VARCHAR,'
        q += 'visit_id INTEGER)'
        db.execute(q)
        q = u'CREATE UNIQUE INDEX id_index ON '
        q += cls.__name__ + ' (id)'
        db.execute(q)
    create_table = classmethod(create_table)
    def drop_table(cls, db):
        q = u'DROP TABLE ' + cls.__name__
        db.execute(q)
    drop_table = classmethod(drop_table)

class TrapsConfig(orm.Mapper):
    class mapping:
        site = orm.column(orm.String)
        ima = orm.column(orm.Integer)
        xcoord = orm.column(orm.Integer)
        ycoord = orm.column(orm.Integer)
        position = orm.column(orm.String)
        barcode = orm.column(orm.String)
    def create_table(cls,db):
        q = u'CREATE TABLE ' + cls.__name__ + ''
        q += '(id COUNTER,'
        q += 'site VARCHAR,'
        q += 'ima INTEGER,'
        q += 'xcoord INTEGER,'
        q += 'ycoord INTEGER,'
        q += 'position VARCHAR,'
        q += 'barcode VARCHAR)'
        db.execute(q)
    create_table = classmethod(create_table)
    def drop_table(cls, db):
        q = u'DROP TABLE ' + cls.__name__
        db.execute(q)
    drop_table = classmethod(drop_table)


def IsInt(str):
    try: int(str)
    except ValueError:return 0
    else: return 1

def CheckDigit(arg):
    weight=[1,3]*6; magic=10; sum = 0
    for i in range(12):         # checksum based on first 12 digits.
        sum = sum + int(arg[i]) * weight[i]
    z = ( magic - (sum % magic) ) % magic
    return z

def CreateBarcode(trap_name):
    hexdigest = md5.new(trap_name).hexdigest()
    barcode = u''
    for c in hexdigest[0:12]:
        if IsInt(c):
            barcode += c
        else:
            # this makes a = 0, b = 1, etc.
            barcode += str(ord(c.lower()) - ord('a'))
    barcode += str(CheckDigit(barcode))
    return barcode

def TrapsPopulate():
    db = e32db.Dbms()
    fn = u'e:\\trapsconfig.db'
    exp_fn = u'e:\\trapsconfig.txt'
    f = open(exp_fn,'w')
    try:
        db.create(fn)
    except:
        pass
    db.open(fn)
    try:
        TrapsConfig.drop_table(db)
    except:
        pass
    TrapsConfig.create_table(db)
    for site in ['CAXI']:
        for ima in range(1,4):
            for (xcoord,ycoord) in [(01,300), (01,900),
                                    (04,000), (04,600)]:
                for position in ['U','C']:
                    # trap_name looks like (after conv. to lower case):
                    # caxi:1:(1,300):u
                    trap_name = site+':'\
                                +str(ima)+':('\
                                +str(xcoord)+','\
                                +str(ycoord)+'):'\
                                +position
                    trap_name = trap_name.lower()
                    barcode = CreateBarcode(trap_name)
                    print "barcode:" + barcode
                    mydict = {'site':site,
                              'ima':ima,
                              'xcoord':xcoord,
                              'ycoord':ycoord,
                              'position':position,
                              'barcode':barcode}
                    trapsconfigORM = TrapsConfig(db,**mydict)
                    f.write(trap_name+';'+barcode+'\n')
    f.close()

                    
    
