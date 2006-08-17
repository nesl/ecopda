import appuifw
import e32
import time

import sys
sys.path.append('e:\\python') #to properly find orm and keyboard
import butterfly_helper
import orm
import keyboard
import e32db

# Read in the DB
db = e32db.Dbms()
db.open(u'e:\\test.db')

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
        family = orm.column(orm.String)
        subfamily = orm.column(orm.String)
        genus = orm.column(orm.String)
        species = orm.column(orm.String)
        sex = orm.column(orm.String)
        recapture = orm.column(orm.String)
        date_of_identification = orm.column(orm.Float)
        identified_by = orm.column(orm.String)
        comments = orm.column(orm.String)
        # image file ?
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
        q += 'family VARCHAR,'
        q += 'subfamily VARHCAR,'
        q += 'genus VARHCAR,'
        q += 'species VARHCAR,'
        q += 'sex VARHCAR,'
        q += 'recapture VARHCAR,'
        q += 'date_of_identification FLOAT,'
        q += 'identified_by VARHCAR,'
        q += 'comments LONG VARHCAR)' 
        db.execute(q)
        q = 'CREATE UNIQUE INDEX id_index ON '
        q += cls.__name__ + ' (id)'
        db.execute(q)
    create_table = classmethod(create_table)
    def drop_table(cls, db):
        q = 'DROP TABLE ' + cls.__name__
        db.execute(q)
    drop_table = classmethod(drop_table)
    

### Capture Object
class Capture:
    def __init__(self, id=None, **kw):
        self.id = id
        # Combos, used by the form
        self.position_combo  = [u'U',u'C']
        self.family_combo    = [u'Nymphalidae', u'Other']
        self.subfamily_combo = [u'Brassolinae',
                                u'Charaxinae',
                                u'Ithomiinae',
                                u'Morphinae',
                                u'Nymphalinae',
                                u'Satyrinae',
                                u'Other']
        self.sex_combo       = [u'F',u'M']
        self.recapture_combo = [u'N',u'Y']

        # Dict of form fields
        self.capture_dict = {
            'site'      : u'', # Caxluana
            'date'      : time.time(), # Seconds since epoch
            'time'       : float((time.gmtime()[3] * 3600 \
                                  + time.gmtime()[4] * 60 + \
                                  + time.gmtime()[5])), # Seconds since midnight
            'ima'       : 0, # The Array ID
            'xcoord'    : 0, # Array X coord
            'ycoord'    : 0, # Array Y coord
            'position'  : u'', # Stratum: Canopy or Understory
            'family'    : u'',
            'subfamily' : u'',
            'genus'     : u'',
            'species'   : u'',
            'sex'       : u'',
            'recapture' : u'',
            'date_of_identification' : 0.0,
            'identified_by' : u'',
            'comments'  : u''}

        # Pick up anything new specified by user.
        self.capture_dict.update(kw)
        
    def create_form_fields(self):
        form_fields = [(u'Site','text',self.capture_dict[u'site']),
                       (u'Date','date', self.capture_dict[u'date']),
                       (u'Time','time',self.capture_dict[u'time']),
                       (u'IMA','number',self.capture_dict[u'ima']),
                       (u'xcoord','number',self.capture_dict[u'xcoord']),
                       (u'ycoord','number',self.capture_dict[u'ycoord']),
                       (u'Position','combo',(self.position_combo,
                                             butterfly_helper.default_combo_index(self.position_combo,
                                                                 self.capture_dict[u'position']))),
                       (u'Family','combo',(self.family_combo,
                                           butterfly_helper.default_combo_index(self.family_combo,
                                                               self.capture_dict[u'family']))),
                       (u'Subfamily','combo',(self.subfamily_combo,
                                              butterfly_helper.default_combo_index(self.subfamily_combo,
                                                                  self.capture_dict[u'subfamily']))),
                       (u'Genus','text',self.capture_dict[u'genus']),
                       (u'Species','text',self.capture_dict[u'species']),
                       (u'Sex','combo',(self.sex_combo,
                                        butterfly_helper.default_combo_index(self.sex_combo,
                                                            self.capture_dict[u'sex']))),
                       (u'Recapture','combo',(self.recapture_combo,
                                              butterfly_helper.default_combo_index(self.recapture_combo,
                                                                  self.capture_dict['recapture']))),
                       (u'Date_of_Identification','date',self.capture_dict['date_of_identification']),
                       (u'Identified_By','text',self.capture_dict['identified_by']),
                       (u'Comments','text',self.capture_dict[u'comments'])]
        return form_fields

    def save_hook(self, form):
        # TODO save to DB
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
            if field_name in self.capture_dict:
                self.capture_dict[field_name] = field_val 
            else:
                appuifw.note(u"bug: " + field_name + " not in dictionary.", "error")

        captureORM = Captures(db, self.id, **self.capture_dict)
        if self.id == None:
            # I was new
            self.id = captureORM.id
        else:
            # I was old. So I have to update the DB
            captureORM.set(**self.capture_dict)
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

    
class CaptureApp:
    # When you switch in, you are shown previous captures:
    # Options:
    #   NEW Capture
    #     NEW When you start your form, your options are Save or cancel.
    #   VIEW Current Capture
    #   EDIT Current Capture
    #   DELETE Current Capture
    
    def __init__(self):
        self.listbox = None
        self.ListID = []
    def switch_in(self):
        # Make selection box showing all previously saved captures.
        # Display ID/Date/Time from newest to oldest.
        # Can I show a picture?
        # Can I do a search box?
        #
        # Menu is
        #    NEW -> (Save/Cancel)
        #    VIEW
        #    EDIT
        #    DELETE

        # Fetch a list of previously saved captures:
        # TODO Try with 'id DESC'

        capture_iter = Captures.select(db, orderby='id DESC') 

        # For each row, Add an id number to the list
        L = [u'Create New']
        self.ListID = [None]
        # TEST
        try:
            while 1:
                captureORM = capture_iter.next()
                L.append(    #unicode(captureORM.id)
                         u' ' + time.ctime( captureORM.date + captureORM.time )
                         + ' GMT')
                self.ListID.append(captureORM.id) 
        except StopIteration:
            pass

        # Create the Listbox
        self.listbox = appuifw.Listbox(L,self.lb_callback)
        # Show it
        appuifw.app.body = self.listbox
        
    def lb_callback(self):
        # If index is == 0, then give the use a new form:
        if self.listbox.current() == 0:
            capture = self.new_capture()
        else:
            # Save the id of the Index,
            # Create a popup selection box that asks for
            # VIEW, EDIT, DELETE
            # TODO
            pop_up_L = [u'View',u'Edit',u'Delete']
            pop_up_index = appuifw.popup_menu(pop_up_L, u"Select Action")
            captureORM = Captures(db,id=self.ListID[self.listbox.current()])
            if pop_up_index == 0: # View
                capture = Capture(**captureORM.dict())
                capture.execute_form(appuifw.FFormViewModeOnly
                                    + appuifw.FFormDoubleSpaced)
            elif pop_up_index == 1: # Edit
                # Create a new form instantiated
                # capturesORM with that ID.
                capture = Capture(**captureORM.dict())
                capture.execute_form()
            elif pop_up_index == 2: # Delete
                # are you sure you want to delete blah?
                # TODO
                captureORM.delete()
                appuifw.note(u"Deleted.")

        # This will update the listbox
        self.switch_in()
        
    def new_capture(self):
        capture = Capture()
        capture.execute_form()
        # At this point, user has exited form.
        
    def switch_out(self):
        return
    

