import appuifw
import e32
import time

import sys
sys.path.append('e:\\python') #to properly find orm and keyboard
import orm
import keyboard

import e32db


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
    

# Returns -1 if no match, otherwise returns index of
# first matching item.
def find_index_of_matching(thelist, target_item):
    index = 0
    for item in thelist:
        if item == target_item:
            return index
        ++index
    return -1

def default_combo_index(thelist, target_item, default_index=0):
    result = find_index_of_matching(thelist, target_item)
    if result == -1:
        result = default_index
    return result

### Capture Object
class Capture:
    def __init__(self, **kw):
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
            u'id'        : None, # this does not appear in the form
            u'site'      : u'', # Caxluana
            u'date'      : time.time(), # Seconds since epoch
            u'time'       : float((time.gmtime()[3] * 3600 \
                                  + time.gmtime()[4] * 60 + \
                                  + time.gmtime()[5])), # Seconds since midnight
            u'ima'       : 0, # The Array ID
            u'xcoord'    : 0, # Array X coord
            u'ycoord'    : 0, # Array Y coord
            u'position'  : u'', # Stratum: Canopy or Understory
            u'family'    : u'',
            u'subfamily' : u'',
            u'genus'     : u'',
            u'species'   : u'',
            u'sex'       : u'',
            u'recapture' : u'',
            u'date_of_identification' : u'',
            u'identified_by' : u'',
            u'comments'  : u''}

        # Pick up anything new specified by user.
        self.capture_dict.update(kw)
        
    def create_form_fields(self):
        form_fields = [(u'Site','text',self.capture_dict[u'site']),
                       (u'Date','date', self.capture_dict[u'date']),
                       (u'Time GMT','time',self.capture_dict[u'time']),
                       (u'IMA#','number',self.capture_dict[u'ima']),
                       (u'xcoord','number',self.capture_dict[u'xcoord']),
                       (u'ycoord','number',self.capture_dict[u'ycoord']),
                       (u'Position','combo',(self.position_combo,
                                             default_combo_index(self.position_combo,
                                                                 self.capture_dict[u'position']))),
                       (u'Family','combo',(self.family_combo,
                                           default_combo_index(self.family_combo,
                                                               self.capture_dict[u'family']))),
                       (u'Subfamily','combo',(self.subfamily_combo,
                                              default_combo_index(self.subfamily_combo,
                                                                  self.capture_dict[u'subfamily']))),
                       (u'Genus','text',self.capture_dict[u'genus']),
                       (u'Species','text',self.capture_dict[u'species']),
                       (u'Sex','combo',(self.sex_combo,
                                        default_combo_index(self.sex_combo,
                                                            self.capture_dict[u'sex']))),
#                        (u'Recapture','combo',(self.recapture_combo,
#                                               default_combo_index(self.recapture_combo,
#                                                                   self.capture_dict['recapture']))),
#                        (u'Date of Classification','date',self.capture_dict['date_of_classification']),
#                        (u'Identified By','text',self.capture_dict['identified_by']),
                       (u'Comments','text',self.capture_dict[u'comments'])]
        return form_fields

    def save_hook(self, form):
        # TODO save to DB
        return 1

    def create_form(self):
        # Set the view/edit mode of the form
        flags = appuifw.FFormEditModeOnly + appuifw.FFormDoubleSpaced
        form_fields = self.create_form_fields()
        # Creates the form
        form = appuifw.Form(form_fields, flags)
        form.save_hook = self.save_hook
        return form


    
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
        capture_iter = Captures.select(db, orderby=u'id') 

        # For each row, Add an id number to the list
        L = [u'Create New']
        try:
            while 1:
                captureORM = capture_iter.next()
                L.append(str(captureORM.id))
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
            if pop_up_index == 0: # View
                #TODO
                appuifw.note(u'TODO View')
            elif pop_up_index == 1: # Edit
                # TODO
                appuifw.note(u'TODO Edit')
            elif pop_up_index == 2: # Delete
                appuifw.note(u'TODO Delete')

        # This will update the listbox
        self.switch_in()
        
    def new_capture(self):
        capture = Capture()
        form = capture.create_form()
        form.execute()
        # At this point, user has exited form.
        
    def switch_out(self):
        return
    


######################
### Main part of application

def exit_key_handler():
    app_lock.signal()

def handle_tab(index):
    if index == 0:
        capture_app.switch_in()

# Create an Active object
app_lock = e32.Ao_lock()
# Set exit key handler
appuifw.app.exit_key_handler = exit_key_handler

# Read in the DB
db = e32db.Dbms()
dbv = e32db.Db_view()
db.open(u'e:\\test.db')

# Create the tabs with its names in unide as a list, include the tab handler
appuifw.app.set_tabs([u'Capture'], handle_tab)

# Create the application objects
capture_app = CaptureApp()

# Set app.body to app1 (for start of script)
handle_tab(0)

app_lock.wait()
