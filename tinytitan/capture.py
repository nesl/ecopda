import appuifw
import e32
import time

import sys
sys.path.append('e:\\python') #to properly find orm and keyboard
import butterfly_helper
import orm
import keyboard
import e32db

import camera
from graphics import *

import audio

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
        picture_filename = orm.column(orm.String)
        audio_filename = orm.column(orm.String)
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
        q += 'subfamily VARCHAR,'
        q += 'genus VARCHAR,'
        q += 'species VARCHAR,'
        q += 'sex VARCHAR,'
        q += 'recapture VARCHAR,'
        q += 'date_of_identification FLOAT,'
        q += 'identified_by VARCHAR,'
        q += 'comments LONG VARCHAR,'
        q += 'picture_filename VARCHAR,'
        q += 'audio_filename VARCHAR)'
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
    def __init__(self, db, id=None, **kw):
        self.db = db
        self.id = id
        self.form = None
        self.picture = None
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
            'date_of_identification' : float(0),
            'identified_by' : u'',
            'comments'  : u'',
            'picture_filename' : u'',
            'audio_filename' : u''}

        # Pick up anything new specified by caller.
        self.capture_dict.update(kw)

    ## NOTE: form field names need to map to dict names,
    ## which need to map to variable names.
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
                       (u'Comments','text',self.capture_dict[u'comments']),
                       (u'Picture Filename','text',self.capture_dict[u'picture_filename']),
                       (u'Audio Filename','text',self.capture_dict[u'audio_filename'])]
        return form_fields

    def save_hook(self, form_list):
        # TODO save to DB
        # form is the user's form.
        # Has the structure [(u'field_name','type','data'), ... ]
        for i in form_list:
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

        captureORM = Captures(self.db, self.id, **self.capture_dict)
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
        self.form = appuifw.Form(form_fields, flags)
        self.form.save_hook = self.save_hook
        return self.form

    def execute_form(self, flags = None):
        self.form = self.create_form(flags)
        self.form.execute()


    
class AudioApp:
    def __init__(self, exit_cb, captureORM):
        self.captureORM = captureORM
        self.filename = u''
        if self.captureORM.audio_filename != None:
            self.filename = self.captureORM.audio_filename
        self.S = None
        self.body = appuifw.Canvas()
        #self.body = appuifw.Text(u'Audio Mode')
        appuifw.app.title = u'Audio Mode'
        
        self.filename_prefix = u'e:\\Sounds\obs_'
        self.exit_cb = exit_cb
    def recording(self):
        self.filename = self.filename_prefix + str(int(time.time())) + u'.wav'
        self.S = audio.Sound.open(self.filename)
        self.S.record()
        self.captureORM.audio_filename = self.filename
        appuifw.note(u"Recording to " + self.filename)
    def playing(self):
        try:
            self.S = audio.Sound.open(self.filename)
            self.S.play()
            appuifw.note(u"Playing " + self.filename)
        except:
            appuifw.note(u"Record something first.")
    def closing(self):
        self.S.stop()
        self.S.close()
        appuifw.note(u"Stopped.")
    def switch_in(self):
        appuifw.app.menu =[(u"play", self.playing),
                           (u"record", self.recording),
                           (u"stop", self.closing),
                           (u"exit", self.switch_out)]
        appuifw.app.title = u'Audio'
        appuifw.app.body = self.body
    def switch_out(self):
        self.exit_cb
        return

    
class CaptureApp:
    # When you switch in, you are shown previous captures:
    # Options:
    #   NEW Capture
    #     NEW When you start your form, your options are Save or cancel.
    #   VIEW Current Capture
    #   EDIT Current Capture
    #   DELETE Current Capture
    
    def __init__(self, db):
        self.listbox = None
        self.ListID = []
        self.db = db
        self.fname = u'e:\\python\\butterfly_data\\captures.xml'
    def switch_in(self):
        appuifw.app.title = u'Capture'

        # create menu:
        appuifw.app.menu = [(u'Export Captures',self.export),
                            (u'Upload Captures',self.upload)]
        
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
        capture_iter = Captures.select(self.db, orderby='id DESC') 

        # For each row, Add an id number to the list
        L = [u'Create New Capture']
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
            pop_up_L = [u'View',u'Edit',u'Delete', u'Take Picture', u'Audio Options']
            pop_up_index = appuifw.popup_menu(pop_up_L, u"Select Action")
            captureORM = Captures(self.db,id=self.ListID[self.listbox.current()])
            if pop_up_index == 0: # View
                capture = Capture(self.db,**captureORM.dict())
                capture.execute_form(appuifw.FFormViewModeOnly
                                    + appuifw.FFormDoubleSpaced)
            elif pop_up_index == 1: # Edit
                # Create a new form instantiated
                # capturesORM with that ID.
                capture = Capture(self.db,**captureORM.dict())
                capture.execute_form()
            elif pop_up_index == 2: # Delete
                # are you sure you want to delete blah?
                # TODO
                captureORM.delete()
                appuifw.note(u"Deleted.")
            elif pop_up_index == 3: # Take Picture
                self.take_picture(captureORM)
            elif pop_up_index == 4: # Take Audio
                self.audio_options(captureORM)
                
        # This will update the listbox
        self.switch_in()
        
    def new_capture(self):
        capture = Capture(self.db)
        capture.execute_form()
        # At this point, user has exited form.
        
    def switch_out(self):
        return
    
    def take_picture(self, captureORM):
        self.screen_picture = camera.take_photo(size = (1280, 960))
        self.img = Image.new((176,208))
        self.canvas = appuifw.Canvas(redraw_callback=self.handle_redraw)
        self.filename_prefix = u'e:\\Images\obs_'
        self.filename = u''
        self.old_body = appuifw.app.body
        appuifw.app.body = self.canvas
        #appuifw.app.menu =[(u"Save Image", self.save_picture)]
        appuifw.app.title = u'Image'
        self.filename = self.filename_prefix + str(int(time.time())) + u'.jpg'
        data = appuifw.query(u"Save this image to " + self.filename,"query")
        if data:
            self.screen_picture.save(self.filename)
            captureORM.picture_filename = self.filename
            appuifw.note(u"Saved." , "conf")
        self.handle_redraw(())
        appuifw.app.body = self.old_body
        
    def audio_options(self, captureORM):
        self.old_body = appuifw.app.body
        self.audioApp = AudioApp(self.audio_exit_cb, captureORM)
        self.audioApp.switch_in()

    def audio_exit_cb(self):
        appuifw.app.body = self.old_body
        appuifw.app.title = u'Capture'
        return
        

    def handle_redraw(self,rect):
          self.img.blit(self.screen_picture, target=(8,10, 168, 130), scale=1)
          self.canvas.blit(self.img)

    def export(self):
        # Select all from the DB.
        # Output header
        # <table>
        # For each row, do:
        #   <row>
        #   For each field name do:
        #     <field name="NAME">VALUE</field>
        #   </row>
        # </table>
        capture_iter = Captures.select(self.db)
        output = u''
        output += '<table>\n'
        try:
            while 1:
                captureORM = capture_iter.next()
                output += captureORM.slog_out()
        except StopIteration:
            output += '</table>'

        f = open(self.fname, 'w')
        f.write(output)
        f.close()
        appuifw.note(u'Wrote to '+ self.fname)

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
            
            
