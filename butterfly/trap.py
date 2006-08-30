import appuifw
import e32
import e32db
import time
import butterfly_helper
from butterflydb import *
import orm
import keyboard
import string

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

    ##currently, save_hook strips off everything before and including the ":"
    def create_form_fields(self):
        form_fields = [
                       (u'1:Date','date', self.trap_dict[u'date']),
                       (u'2:Time','time',self.trap_dict[u'time']),
                       (u'3:Date_of_First_Baiting','date',self.trap_dict[u'date_of_first_baiting']),
                       (u'4:Height','float',self.trap_dict[u'height']),
                       (u'5:Temperature','float',self.trap_dict[u'temperature']),
                       (u'6:Humidity','float',self.trap_dict[u'humidity']),
                       (u'7:Wind_Speed','float',self.trap_dict[u'wind_speed']),
                       (u'8:Date_of_Bait_Prep','date',self.trap_dict[u'date_of_bait_prep']),
                       (u'9:Date_of_Bait_Refill','date',self.trap_dict[u'date_of_bait_refill']),
                       (u'10:Canopy_Cover','combo',(self.canopy_cover_combo,
                                                 butterfly_helper.default_combo_index(self.canopy_cover_combo,
                                                                                      self.trap_dict[u'canopy_cover']))),
                       (u'11:Collectors','text',self.trap_dict[u'collectors']),
                       (u'12:Comments','text',self.trap_dict[u'comments'])
                        ]
        return form_fields
    def save_hook(self, form):
        # form is the user's form.
        # Has the structure [(u'field_name','type','data'), ... ]
        self.form = form
        for i in self.form:
            field_name = str(i[0]).lower()
            field_name = field_name[ ( string.find(field_name,":")+1 ) : ]
            field_name = field_name.lower()
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
            appuifw.note(u'I am new')
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

    def execute_form(self, flags = None):
        self.create_form(flags)
        self.form.execute()

        
class TrapApp:
    def __init__(self,butterfly_app, db):
        self.butterfly_app = butterfly_app
        self.listbox = None
        self.ListID = []
        self.db = db
        self.fname = u'e:\\butterfly_data\\traps.xml'
        self.selected = 0
        self.viewby = 'date Desc'
        self.child_db =[] # this must be set from outside
        self.dbv = e32db.Db_view()
        self.parent_dict = {}
    def view(self, column, orderby=''):
        self.viewby = column + orderby
        self.switch_in()
        return
    def number_of_traps(self):
        #try to calculate the number of rows in the db
        self.dbv.prepare(self.db, u'SELECT * from Traps')
        numrows=self.dbv.count_line()
        appuifw.note(u'# of Traps: ' + unicode(numrows))        
    def ave_captures_per_trap(self):
        return
    def switch_in(self):
        try:
            Traps.create_table(self.db)
        except:
            pass
        appuifw.app.title = unicode(self.parent_dict['site']
                                    +':'+str(self.parent_dict['ima'])
                                    +':('+str(self.parent_dict['xcoord'])
                                    +','+str(self.parent_dict['ycoord'])
                                    +'):'+self.parent_dict['position'])
        appuifw.app.menu = self.butterfly_app.menu_items()                            
        menu = [(u'Table',
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
        for x in menu:
            appuifw.app.menu.append(x)
        where_query = u"(site = '" + self.parent_dict['site'] + "'"
        where_query += u" AND ima=" + str(self.parent_dict['ima'])
        where_query += u" AND xcoord=" + str(self.parent_dict['xcoord'])
        where_query += u" AND ycoord=" + str(self.parent_dict['ycoord'])
        where_query += u" AND position='" + str(self.parent_dict['position']) + "'"
        where_query += ')'
        trap_iter = Traps.select(self.db, where=where_query, orderby='id DESC') 
        L = [u'New Visit / Show all']
        self.ListID = [None]
        try:
            while 1:
                trapORM = trap_iter.next()
                if (-1 < string.find(self.viewby, 'date')):
                    L.append(u' ' + time.ctime( trapORM.date + trapORM.time )
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
        self.switch_in()

    def new_trap(self):
        #self.parent_dict has an id field already, make it = None
        self.parent_dict['id']=None
        trap = Trap(self.db, **(self.parent_dict))
        trap.execute_form()
        
    def switch_out(self):
        try:
            self.selected=self.listbox.current()
        except:
            self.selected=1
        if (self.selected == 0):
            return -1
            #return -1 to select all traps, else return the id for the currently selected one
        trapORM = Traps(self.db,id=self.ListID[self.listbox.current()])
        #trapORM is a dictionary
        returnval = trapORM.id
        return returnval

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



