import appuifw
import e32
import time
import string

import sys
sys.path.append('e:\\python') #to properly find orm and keyboard
import butterfly_helper
from butterflydb import *
import orm
import keyboard
import e32db

import camera
from graphics import *

import audio

# This is the ORM to the table 'Captures'
# class Captures(orm.Mapper):
#     class mapping:
#         site = orm.column(orm.String)
#         date = orm.column(orm.Float) # try this with TIMESTAMP later?
#         time = orm.column(orm.Float) # try this with TIMESTAMP later?
#         ima = orm.column(orm.Integer)
#         xcoord = orm.column(orm.Integer)
#         ycoord = orm.column(orm.Integer)
#         position = orm.column(orm.String)
#         specimen_code = orm.column(orm.String)
#         family = orm.column(orm.String)
#         subfamily = orm.column(orm.String)
#         genus = orm.column(orm.String)
#         species = orm.column(orm.String)
#         sex = orm.column(orm.String)
#         recapture = orm.column(orm.String)
#         date_of_identification = orm.column(orm.Float)
#         identified_by = orm.column(orm.String)
#         comments = orm.column(orm.String)
#         picture_filename = orm.column(orm.String)
#         audio_filename = orm.column(orm.String)
#     def create_table(cls, db):
#         q = u'CREATE TABLE ' + cls.__name__ + ' '
#         q += '(id COUNTER,'
#         q += 'site VARCHAR,'
#         q += 'date FLOAT,'
#         q += 'time FLOAT,'
#         q += 'ima INTEGER,'
#         q += 'xcoord INTEGER,'
#         q += 'ycoord INTEGER,'
#         q += 'position VARCHAR,'
#         q += 'specimen_code VARCHAR,'
#         q += 'family VARCHAR,'
#         q += 'subfamily VARCHAR,'
#         q += 'genus VARCHAR,'
#         q += 'species VARCHAR,'
#         q += 'sex VARCHAR,'
#         q += 'recapture VARCHAR,'
#         q += 'date_of_identification FLOAT,'
#         q += 'identified_by VARCHAR,'
#         q += 'comments LONG VARCHAR,'
#         q += 'picture_filename VARCHAR,'
#         q += 'audio_filename VARCHAR)'
#         db.execute(q)
#         q = u'CREATE UNIQUE INDEX id_index ON '
#         q += cls.__name__ + ' (id)'
#         db.execute(q)
#     create_table = classmethod(create_table)
#     def drop_table(cls, db):
#         q = u'DROP TABLE ' + cls.__name__
#         db.execute(q)
#     drop_table = classmethod(drop_table)
    

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
        #self.ima = ima
        self.picture_filename = u''
        if u'picture_filename' in kw:
            self.picture_filename = kw['picture_filename']
        
        
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
            'specimen_code' : u'',
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
            'audio_filename' : u'',
            'visit_id' : 0}

        # Pick up anything new specified by caller.
        try: del kw['date']
        except: pass
        try: del kw['time']
        except: pass
        for k in kw.keys():
            if k in self.capture_dict:
                self.capture_dict[k] = kw[k]

#         appuifw.popup_menu([unicode(self.capture_dict['site']
#                                     +':'+str(self.capture_dict['ima'])
#                                     +':('+str(self.capture_dict['xcoord'])
#                                     +','+str(self.capture_dict['ycoord'])
#                                     +'):'+self.capture_dict['position'])],
#                            u'From Capture.__init__')


    ## NOTE: form field names need to map to dict names,
    ## which need to map to variable names.
    ##currently, save_hook strips off everything before and including the ":"
    def create_form_fields(self):
        form_fields = [
#                       (u'Site','text',self.capture_dict[u'site']),
                       (u'1:Date','date', self.capture_dict[u'date']),
                       (u'2:Time','time',self.capture_dict[u'time']),
#                       (u'IMA','number',self.capture_dict[u'ima']),
#                       (u'xcoord','number',self.capture_dict[u'xcoord']),
#                       (u'ycoord','number',self.capture_dict[u'ycoord']),
#                       (u'Position','combo',(self.position_combo,
 #                                            butterfly_helper.default_combo_index(self.position_combo,
 #                                                                self.capture_dict[u'position']))),
                       (u'3:Specimen_Code','text',self.capture_dict[u'specimen_code']),
                       (u'4:Family','combo',(self.family_combo,
                                           butterfly_helper.default_combo_index(self.family_combo,
                                                               self.capture_dict[u'family']))),
                       (u'5:Subfamily','combo',(self.subfamily_combo,
                                              butterfly_helper.default_combo_index(self.subfamily_combo,
                                                                  self.capture_dict[u'subfamily']))),
                       (u'6:Genus','text',self.capture_dict[u'genus']),
                       (u'7:Species','text',self.capture_dict[u'species']),
                       (u'8:Sex','combo',(self.sex_combo,
                                        butterfly_helper.default_combo_index(self.sex_combo,
                                                            self.capture_dict[u'sex']))),
                       (u'9:Recapture','combo',(self.recapture_combo,
                                              butterfly_helper.default_combo_index(self.recapture_combo,
                                                                  self.capture_dict['recapture']))),
                       (u'10:Date_of_Identification','date',self.capture_dict['date_of_identification']),
                       (u'11:Identified_By','text',self.capture_dict['identified_by']),
                       (u'12:Comments','text',self.capture_dict[u'comments'])
#                       (u'Picture_Filename','text',self.capture_dict[u'picture_filename']),
#                       (u'Audio_Filename','text',self.capture_dict[u'audio_filename'])
                        ]
        return form_fields

    def save_hook(self, form_list):
        # TODO save to DB
        # form is the user's form.
        # Has the structure [(u'field_name','type','data'), ... ]
        for i in form_list:
            field_name = str(i[0]).lower()
            field_name = field_name[ ( string.find(field_name,":")+1 ) : ]
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

        # Check for self.picture_filename
        if self.picture_filename is not u'':
            self.capture_dict['picture_filename'] = self.picture_filename

#         appuifw.popup_menu([unicode(self.capture_dict['site']
#                                     +':'+str(self.capture_dict['ima'])
#                                     +':('+str(self.capture_dict['xcoord'])
#                                     +','+str(self.capture_dict['ycoord'])
#                                     +'):'+self.capture_dict['position'])],
#                            u'From save_hook')
        
        captureORM = Captures(self.db, self.id, **self.capture_dict)
        if self.id == None:
            # I was new
            appuifw.note(u'I am new')
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
        self.form = appuifw.Form(form_fields,flags)
        self.form.save_hook = self.save_hook
        self.form.menu = [(u'Apply Picture', self.apply_picture_filename),
                          (u'View Picture', self.view_picture_filename)]
        return self.form

    def execute_form(self, flags = None):
        self.form = self.create_form(flags)
        self.form.execute()

    def apply_picture_filename(self):
        self.picture_filename = butterfly_helper.get_newest_image_name()
        appuifw.note(u"Applying: " + self.picture_filename)
        self.save_hook(self.form)

    def view_picture_filename(self):
        self.img = Image.new((400,400))
        self.screen_picture = Image.open(self.picture_filename)
        self.canvas = appuifw.Canvas(redraw_callback=self.handle_redraw)
        self.old_body = appuifw.app.body
        appuifw.app.title = u'Image'
        appuifw.app.menu = [(u"Close", self.close_picture)]
        appuifw.app.body = self.canvas
        self.handle_redraw(())


    def close_picture(self):
        appuifw.app.body = self.old_body

    def handle_redraw(self,rect):
        self.img.blit(self.screen_picture,target=(8,10,336,260),scale=1)
        self.canvas.blit(self.img)
        return
    
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
    
    def __init__(self, butterfly_app, db):
        self.butterfly_app = butterfly_app
        self.listbox = None
        self.ListID = []
        self.db = db
        self.fname = u'e:\\butterfly_data\\captures.xml'
        self.selection = -1 # -1 for all -2 for orphans
        self.mass_delete_id = -1
        self.parent_dict = {}
        self.viewby = 'date DESC'
    def show_orphans(self):
        self.selection = -2
        self.switch_in()
    def view(self, column, orderby=''):
        self.viewby = column + orderby
        self.switch_in()
    def number_of_traps(self):
        return
    def ave_captures_per_trap(self):
        return
    def switch_in(self):
        titlestr= u''
#         if (self.selection == -1):
#             titlestr = unicode('All')
#         elif (self.selection == -2):
#             titlestr = unicode('Orphans')
#         else:
#             titlestr = unicode(str(self.selection) + ':')
#         titlestr += unicode(' View: '+self.viewby)
        if self.valid_parent_id():
            appuifw.app.title = unicode(self.parent_dict['site']
                                        +':'+str(self.parent_dict['ima'])
                                        +':('+str(self.parent_dict['xcoord'])
                                        +','+str(self.parent_dict['ycoord'])
                                        +'):'+self.parent_dict['position']
                                        +'\n'+ time.ctime(self.parent_dict['date'] + self.parent_dict['time']))

        else:
            appuifw.app.title = u'ALL Captures for this visit'

        # create menu:
        menu = [(u'Table',
                 ((u'Export Captures', self.export),
                  (u'Upload Captures', self.upload),
                  (u'Reset Captures Table', self.reset_captures_table))),
                (u'Delete Row', self.delete_row),
                (u'View',
                 ((u'Date',lambda x = None: self.view(column='date', orderby='DESC')),
                  (u'IMA',lambda x = None: self.view(column='ima', orderby='DESC')),
                  (u'SITE',lambda x = None: self.view(column='site', orderby='DESC')))),
                (u'Statistics',
                 ((u'Number of Captures', self.number_of_traps),
                  (u'Average Captures per Trap', self.ave_captures_per_trap)))]
        appuifw.app.menu = self.butterfly_app.menu_items()
        for x in menu:
            appuifw.app.menu.append(x)
        
        
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
#        capture_iter = Captures.select(self.db, orderby='id DESC')
        where_query = u""
        if self.valid_parent_id():
            where_query = u"("
            where_query += u"visit_id = " + str(self.parent_dict['id'])
            where_query += ")"
        else: # we must be viewing all captures for that trap
            temp_dict = self.butterfly_app.trap_app.parent_dict
            where_query = u"(site = '" + temp_dict['site'] + "'"
            where_query += u" AND ima=" + str(temp_dict['ima'])
            where_query += u" AND xcoord=" + str(temp_dict['xcoord'])
            where_query += u" AND ycoord=" + str(temp_dict['ycoord'])
            where_query += u" AND position='" + str(temp_dict['position']) + "'"
            where_query += ')'
            
        capture_iter = Captures.select(self.db, where=where_query, orderby='id DESC') 
#         if (self.selection == -2):
#             capture_iter = Captures.select(self.db, where='(ima <> 1 AND ima <> 0)' )
        # For each row, Add an id number to the list
        L = [u'Viewing All']
        if self.valid_parent_id():
            L = [u'Create New']
        self.ListID = [None]
        # TEST
        try:
            while 1:
                captureORM = capture_iter.next()
                if (-1 < string.find(self.viewby, 'date')):
                    L.append(    #unicode(captureORM.id) +
                         u' ' + time.ctime( captureORM.date + captureORM.time )
                         + ' GMT')
                elif (-1 < string.find(self.viewby, 'id')):
                    L.append( unicode(captureORM.id) )
                elif (-1 < string.find(self.viewby, 'ima')):
                    L.append( unicode(captureORM.ima) )
                elif (-1 < string.find(self.viewby, 'site')):
                    L.append( unicode(captureORM.site) )
                elif (-1 < string.find(self.viewby, 'type') ):
                    L.append( unicode(captureORM.family_combo) + u': ' + unicode(captureORM.subfamily_combo) )
                else:
                    L.append(u'bug, invalid viewby type')  
                self.ListID.append(captureORM.id) 
        except StopIteration:
            pass
        # Create the Listbox
        self.listbox = appuifw.Listbox(L,self.lb_callback)
        # Show it
        appuifw.app.body = self.listbox

    def reset_captures_table(self):
        Captures.drop_table(self.db)
        Captures.create_table(self.db)
        self.switch_in()
        appuifw.note(u'Reset Captures table')
    
    def delete_row(self):
        if (self.listbox.current() == 0):
            return
        else:
            captureORM = Captures(self.db,id=self.ListID[self.listbox.current()])
            captureORM.delete()
            appuifw.note(u"Deleted")
            self.switch_in()
            
    def lb_callback(self):
        # If index is == 0, then give the use a new form:
        if (self.listbox.current() == 0):
            if self.valid_parent_id():
                capture = self.new_capture()
        else:
            # Save the id of the Index,
            # Create a popup selection box that asks for
            # VIEW, EDIT, DELETE
            # TODO
#             pop_up_L = [u'View',u'Edit',u'Delete', u'Take Picture', u'Audio Options']
#             pop_up_index = appuifw.popup_menu(pop_up_L, u"Select Action")
            captureORM = Captures(self.db,id=self.ListID[self.listbox.current()])
            # Create a new form instantiated
            # capturesORM with that ID.
            capture = Capture(self.db,**captureORM.dict())
            capture.execute_form()
#             elif pop_up_index == 2: # Delete
#                 # are you sure you want to delete blah?
#                 # TODO
#                 captureORM.delete()
#                 appuifw.note(u"Deleted.")
#             elif pop_up_index == 3: # Take Picture
#                 self.take_picture(captureORM)
#             elif pop_up_index == 4: # Take Audio
#                 self.audio_options(captureORM)
                
        # This will update the listbox
        self.switch_in()

    def mass_delete_on_id(self):
        #will have set self.mass_delete_id beforehand
        capture_iter = Captures.select(self.db, where='ima = '+str(self.mass_delete_id), orderby='id DESC')
        try:
            deletelist=[]
            while 1:
                captureORM = capture_iter.next()
                deletelist+=[captureORM]
        except StopIteration:
            pass
        for x in deletelist:
            appuifw.note(u"Deleting capture "+unicode(time.ctime( x.date + x.time )))
            x.delete()
        

    def new_capture(self):
#         if (self.selection == -1):
#             capture = Capture(self.db)
#         else:
#             capture = Capture(self.db, ima=self.selection)
        # pass in parent's dictionary:
        temp_dict = self.parent_dict.copy()
        try:
            temp_dict['id'] = None
        except:
            pass
        temp_dict['visit_id'] = self.parent_dict['id']
        capture = Capture(self.db, **temp_dict)
        capture.execute_form()
        # At this point, user has exited form.
        
    def switch_out(self):
        # Find out the id of our current selected capture.
        # Create a dictionary representation of that capture.
        # Return it.
        if self.listbox.current() is not 0:
            captureORM = Captures(self.db,id=self.ListID[self.listbox.current()])
            return captureORM.dict()
        else:
            return {}
    
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
        import base64
        capture_iter = Captures.select(self.db)
        f = open(self.fname, 'w')
        try:
            f.write('<table>\n')
            while 1:
                captureORM = capture_iter.next()
                mydict = captureORM.dict()
                # replace copy out audio_filename and picture_filename
                # replace with audio_file and picture_file
                picture_filename = mydict['picture_filename']
                del mydict['picture_filename']
                audio_filename = mydict['audio_filename']
                del mydict['audio_filename']
                record_id = u'Rec ID' + unicode(mydict['id']) + u'\n'
                appuifw.note(record_id + 'Exporting')

                f.write('\t<row>\n')
                f.write(captureORM.slog_out(mydict=mydict))

                picture_file_handle = None
                picture_b64 = u''
                audio_file_handle = None
                audio_b64 = u''
                

                try:
                    fh = open(picture_filename)
                    appuifw.note(record_id + u'Encoding:'+picture_filename)
                    f.write('\t\t<field name="picture">')
                    base64.encode(fh,f)
                    fh.close()
                    f.write('</field>\n')
                except:
                    pass
                try:
                    fh = open(audio_filename)
                    appuifw.note(record_id + u'Encoding:'+audio_filename)
                    f.write('\t\t<field name="audio">')
                    base64.encode(fh,f)
                    fh.close()
                    f.write('</field>\n')
                except:
                    pass

                f.write('\t</row>\n')
        except StopIteration:
            f.write('</table>')
        
        f.close()
        appuifw.note(record_id + u'Wrote to '+ self.fname)

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
        params['tableName']='Captures'
        
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
        f = open(u'e:\\sb_response.html','w')
        f.write(responseText)
        conn.close()
        t2 = time.time()
        appuifw.query((u'response: '+str(response.status) + '\n'
                      + u'time: '+ str((t2-t1)*1000.) + '\n'),"query")
#                       + responseText),
#                       "query")

    def valid_parent_id(self):
        try:
            if self.parent_dict['id'] >= 0:
                return 1
        except:
            pass
        return 0

