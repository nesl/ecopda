import appuifw
import e32
import e32db
import time
import butterfly_helper
import orm
import keyboard
import string

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

def barcode_start():
    import socket
    host = '127.0.0.1'
    port = 88
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.close()


        
### Trap Object
class Trap:
    def __init__(self, db, id=None, **kw):
        self.db = db
        self.id = id
        self.form = None
        # Combos:
        self.position_combo  = [u'U',u'C']
        self.canopy_cover_combo = [u'Closed/semi-closed',
                                   u'Open/treefall gap']
        # Dict of form fields
        self.trap_dict = {
            'site'              : u'',
            'date'              : time.time(), # Seconds since epoch
            'time'              : float((time.gmtime()[3] * 3600 \
                                  + time.gmtime()[4] * 60 + \
                                  + time.gmtime()[5])), # Seconds since midnight
            'ima'               : 0, # The Array ID
            'xcoord'            : 0, # Array X coord
            'ycoord'            : 0, # Array Y coord
            'position'          : u'', # Stratum: Canopy or Understory
            'date_of_first_baiting' : time.time(),
            'height'            : float(0),
            'temperature'       : float(0),
            'humidity'          : float(0),
            'wind_speed'        : float(0),
            'date_of_bait_prep' : time.time(),
            'date_of_bait_refill' : float(0),
            'canopy_cover'      : u'',
            'collectors'        : u'',
            'comments'          : u'',
            'barcode'           : u''}
        # Pick up anything new specified by the caller.
        self.trap_dict.update(kw)

    def create_form_fields(self):
        form_fields = [(u'Site','text',self.trap_dict[u'site']),
                       (u'Date','date', self.trap_dict[u'date']),
                       (u'Time','time',self.trap_dict[u'time']),
                       (u'IMA','number',self.trap_dict[u'ima']),
                       (u'xcoord','number',self.trap_dict[u'xcoord']),
                       (u'ycoord','number',self.trap_dict[u'ycoord']),
                       (u'Position','combo',(self.position_combo,
                                             butterfly_helper.default_combo_index(self.position_combo,
                                                                                  self.trap_dict[u'position']))),
                       (u'Date_of_First_Baiting','date',self.trap_dict[u'date_of_first_baiting']),
                       (u'Height','float',self.trap_dict[u'height']),
                       (u'Temperature','float',self.trap_dict[u'temperature']),
                       (u'Humidity','float',self.trap_dict[u'humidity']),
                       (u'Wind_Speed','float',self.trap_dict[u'wind_speed']),
                       (u'Date_of_Bait_Prep','date',self.trap_dict[u'date_of_bait_prep']),
                       (u'Date_of_Bait_Refill','date',self.trap_dict[u'date_of_bait_refill']),
                       (u'Canopy_Cover','combo',(self.canopy_cover_combo,
                                                 butterfly_helper.default_combo_index(self.canopy_cover_combo,
                                                                                      self.trap_dict[u'canopy_cover']))),
                       (u'Collectors','text',self.trap_dict[u'collectors']),
                       (u'Comments','text',self.trap_dict[u'comments']),
                       (u'Barcode','text',self.trap_dict[u'barcode'])]
        return form_fields
    def save_hook(self, form):
        # form is the user's form.
        # Has the structure [(u'field_name','type','data'), ... ]
        self.form = form
        for i in self.form:
            field_name = str(i[0]).lower()
            field_val = None
            if (i[1] != 'combo'):
                field_val = i[2]
            else: # this is how you deal with combos
                List, Index = i[2]
                field_val = List[Index]
            if field_name in self.trap_dict:
                self.trap_dict[field_name] = field_val 
            else:
                appuifw.note(u"bug: " + field_name + " not in dictionary.", "error")

        trapORM = Traps(self.db, self.id, **self.trap_dict)
        if self.id == None:
            # I was new
            self.id = trapORM.id
        else:
            # I was old. So I have to update the DB
            trapORM.set(**self.trap_dict)
        appuifw.note(u"Saved to DB row id:" + str(self.id), "conf")

    def create_form(self, flags = None):
        # Set the view/edit mode of the form
        if not flags:
            flags = appuifw.FFormEditModeOnly + appuifw.FFormDoubleSpaced
        form_fields = self.create_form_fields()
        # Creates the form
        self.form = appuifw.Form(form_fields, flags)
        self.form.save_hook = self.save_hook
        self.form.menu = [(u'Launch Barcode Reader', barcode_start),
                          (u'Accept Barcode', self.barcode_read)]


    def execute_form(self, flags = None):
        self.create_form(flags)
        self.form.execute()

    def barcode_read(self):
        barcodefile = u'e:\\mylog.txt'
        barcode_result = u''
        f = open(barcodefile)
        try:
            barcode_result = self.stupid(f.read())
            appuifw.note(u'barcode: ' + barcode_result)
        except:
            appuifw.note(u'unable to read: ' + barcodefile)
        f.close()
        # need to modify self.form
        titles = [title for (title,type,value) in self.form]
        barcode_index = butterfly_helper.find_index_of_matching(titles, 'Barcode')
        if barcode_index is not -1:
            self.form[barcode_index] = (u'Barcode',
                                        u'text',
                                        unicode(barcode_result))
        
class TrapApp:
    def __init__(self,db):
        self.listbox = None
        self.ListID = []
        self.db = db
        self.fname = u'e:\\butterfly_data\\traps.xml'
        self.selected = 0
        self.viewby = 'id Desc'
        self.child_db =[] # this must be set from outside
    def view(self, column, orderby=''):
        self.viewby = column + orderby
        self.switch_in()
        return
    def number_of_traps(self):
        return
    def ave_captures_per_trap(self):
        return
    def switch_in(self):
        try:
            Traps.create_table(self.db)
        except:
            pass
        appuifw.app.title = u'View: '+unicode(self.viewby)
        appuifw.app.menu = [(u'Table',
                             ((u'Export Traps', self.export),
                              (u'Upload Traps', self.upload),
                              (u'Reset Traps Table', self.reset_traps_table))),
                            (u'Delete Row', self.delete_row),
                            (u'View',
                             ((u'Date',lambda x = None: self.view(column='date', orderby='DESC')),
                              (u'IMA',lambda x = None: self.view(column='ima', orderby='DESC')),
                              (u'SITE',lambda x = None: self.view(column='site', orderby='DESC')))),
                            (u'Statistics',
                             ((u'Number of Traps', self.number_of_traps),
                              (u'Average Captures per Trap', self.ave_captures_per_trap)))]
        trap_iter = Traps.select(self.db, orderby='id DESC') 
        L = [u'New Trap / Show all']
        self.ListID = [None]
        try:
            while 1:
                trapORM = trap_iter.next()
                if (-1 < string.find(self.viewby, 'date')):
                    L.append(    #unicode(trapORM.id)
                         u' ' + time.ctime( trapORM.date + trapORM.time )
                         + ' GMT')
                elif (-1 < string.find(self.viewby, 'id')):
                    L.append(unicode(trapORM.id))
                elif (-1 < string.find(self.viewby, 'ima')):
                    L.append(unicode(trapORM.ima))
                elif (-1 < string.find(self.viewby, 'site')):
                    L.append(unicode(trapORM.site))
                else:
                    L.append(u'bug, invalid view type')
                self.ListID.append(trapORM.id) 
        except StopIteration:
            pass
        self.listbox = appuifw.Listbox(L,self.lb_callback)
        appuifw.app.body = self.listbox
    
    def delete_row(self):
        if (self.listbox.current() == 0):
            return
        else:
            trapORM = Traps(self.db,id=self.ListID[self.listbox.current()])
            self.child_db.mass_delete_id = trapORM.id
            self.child_db.mass_delete_on_id()
            trapORM.delete()
            appuifw.note(u"Deleted.")
            self.switch_in()

    def lb_callback(self):
        if self.listbox.current() == 0:
            trap = self.new_trap()
        else:
            trapORM = Traps(self.db,id=self.ListID[self.listbox.current()])
            trap = Trap(self.db,**trapORM.dict())
            trap.execute_form()
#           elif pop_up_index == 2: # Apply Barcode
#                 trapORM.set(barcode = self.barcode_read())
#           elif pop_up_index == 3: # Delete
#                 self.child_db.mass_delete_id = trapORM.id
#                 self.child_db.mass_delete_on_id()
#                 trapORM.delete()
#                 appuifw.note(u"Deleted.")
        self.switch_in()
    def new_trap(self):
        trap = Trap(self.db)
        trap.execute_form()
    def switch_out(self):
        self.selected=self.listbox.current()
        if (self.selected == 0):
            return -1
            #return -1 to select all traps, else return the id for the currently selected one
        trapORM = Traps(self.db,id=self.ListID[self.listbox.current()])
        #trapORM is a dictionary
        returnval = trapORM.id
        return returnval

    def stupid(self, barcode_result):
        result = ""
        for e in barcode_result:
            if e != '\x00':
                result += e
        return result
    

    def barcode_read(self):
        barcodefile = u'e:\\mylog.txt'
        barcode_result = None

        f = open(barcodefile)
        try:
            barcode_result = self.stupid(f.read())
            appuifw.note(u'barcode: ' + barcode_result)
        except:
            appuifw.note(u'unable to read: ' + barcodefile)
        f.close()
        return barcode_result
        

    def reset_traps_table(self):
        Traps.drop_table(self.db)
        Traps.create_table(self.db)
        self.switch_in()
        appuifw.note(u'Reset Traps table')

    def export(self):
        trap_iter = Traps.select(self.db)
        output = u''
        output += '<table>\n'
        try:
            while 1:
                trapORM = trap_iter.next()
                output += '\t<row>\n'
                output += trapORM.slog_out()
                output += '\t</row>\n'
        except StopIteration:
            output += '</table>'
        f = open(self.fname, 'w')
        f.write(output)
        f.close()
        appuifw.note(u'Wrote to '+ self.fname)

    def upload(self):
        import httplib, urllib

        params = {}
        params['email']='adparker@gmail.com'
        params['pw']='ecopda'
        fh = open(self.fname)
        xml = fh.read()
        fh.close()
        params['data_string']= xml
        params['type']='xml'
        params['project_id']="24"
        params['tableName']='Traps'
        
        t1 = time.time()
        params = urllib.urlencode(params)
        t2 = time.time()
        
        appuifw.note(u'URL Encode Time:' + str(((t2-t1)*1000.)))
        
        headers = {}
        headers['Content-type']='application/x-www-form-urlencoded'
        headers['Accept']='text/plain'

        t1 = time.time()
        conn = httplib.HTTPConnection("sensorbase.org")
        conn.request("POST", "/alpha/upload.php", params, headers)
        response = conn.getresponse()
        responseText = response.read()
        conn.close()
        t2 = time.time()
        appuifw.note(u'response: '+str(response.status) + '\n'
                     + u'time: '+ str((t2-t1)*1000.))



