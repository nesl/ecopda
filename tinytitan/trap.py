import appuifw
import e32
import e32db
import time
import butterfly_helper
import orm
import keyboard

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
        # TODO image file?
    def create_table(cls, db):
        q = 'CREATE TABLE ' + cls.__name__ + ' '
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
        q += 'comments LONG VARCHAR)' 
        db.execute(q)
        q = 'CREATE UNIQUE INDEX id_index ON '
        q += cls.__name__ + ' (id)'
        db.execute(q)
    create_table = classmethod(create_table)
    def drop_table(cls, db):
        q = 'DROP TABLE ' + cls.__name__
        db.execute(q)
    drop_table = classmethod(drop_table)

        
### Trap Object
class Trap:
    def __init__(self, db, id=None, **kw):
        self.db = db
        self.id = id
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
            'comments'          : u''}
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
                       (u'Comments','text',self.trap_dict[u'comments'])]
        return form_fields
    def save_hook(self, form):
        # form is the user's form.
        # Has the structure [(u'field_name','type','data'), ... ]
        for i in form:
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
        form = appuifw.Form(form_fields, flags)
        form.save_hook = self.save_hook
        return form

    def execute_form(self, flags = None):
        form = self.create_form(flags)
        form.execute()

class TrapApp:
    def __init__(self,db):
        self.listbox = None
        self.ListID = []
        self.db = db
        self.fname = u'e:\\python\\butterfly_data\\traps.xml'
    def switch_in(self):
        appuifw.app.title = u'Trap Device'
        appuifw.app.menu = [(u'Export Traps', self.export),
                            (u'Upload Traps', self.upload)]
        trap_iter = Traps.select(self.db, orderby='id DESC') 
        L = [u'Create New Trap']
        self.ListID = [None]
        try:
            while 1:
                trapORM = trap_iter.next()
                L.append(    #unicode(trapORM.id)
                         u' ' + time.ctime( trapORM.date + trapORM.time )
                         + ' GMT')
                self.ListID.append(trapORM.id) 
        except StopIteration:
            pass
        self.listbox = appuifw.Listbox(L,self.lb_callback)
        appuifw.app.body = self.listbox
    def lb_callback(self):
        if self.listbox.current() == 0:
            trap = self.new_trap()
        else:
            pop_up_L = [u'View',u'Edit',u'Delete']
            pop_up_index = appuifw.popup_menu(pop_up_L, u"Select Action")
            trapORM = Traps(self.db,id=self.ListID[self.listbox.current()])
            if pop_up_index == 0: # View
                trap = Trap(self.db,**trapORM.dict())
                trap.execute_form(appuifw.FFormViewModeOnly
                                    + appuifw.FFormDoubleSpaced)
            elif pop_up_index == 1: # Edit
                trap = Trap(self.db,**trapORM.dict())
                trap.execute_form()
            elif pop_up_index == 2: # Delete
                trapORM.delete()
                appuifw.note(u"Deleted.")
        self.switch_in()
    def new_trap(self):
        trap = Trap(self.db)
        trap.execute_form()
    def switch_out(self):
        return

    def export(self):
        trap_iter = Traps.select(self.db)
        output = u''
        output += '<table>\n'
        try:
            while 1:
                trapORM = trap_iter.next()
                output += trapORM.slog_out()
        except StopIteration:
            output += '</table>'
        fname = u'e:\\python\\butterfly_data\\traps.xml'
        f = open(fname, 'w')
        f.write(output)
        f.close()
        appuifw.note(u'Wrote to '+ fname)

    def upload(self):
        # upload to www.leninsgodson.com /courses/pys60/php/set_text.php
        import httplib, urllib
        url = "www.leninsgodson.com"
        headers = {"Content-type": "application/xml"}
        fname_handle = open(self.fname)
        data = fname_handle.read()
        fname_handle.close()
        try:
            conn = httplib.HTTPConnection(url)
            conn.request("POST","/courses/pys60/php/set_text.php", data, headers)
            response = conn.getresponse()
            conn.close()
            appuifw.note(u'Response: '+str(response.status))
        except IOError,(errno, sterror):
            appuifw.note(u'I/O Error(%s)' % (errno,strerror))



