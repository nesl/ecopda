import appuifw
import e32
import time
import string
import butterfly_helper
from butterflydb import *
import orm
import keyboard
import e32db
import camera
from graphics import *
import butterflydb

class AttachmentApp:
    def __init__(self,butterfly_app,db):
        self.butterfly_app = butterfly_app
        self.listbox = None
        self.parent_db = {}
        self.selection = 0
        self.db = db
        self.L = []


        # This assumes that parent_db is valid
    def switch_in(self, parent_db):
        self.parent_db = parent_db
        
        if not self.valid_parent_id():
            appuifw.note(u"Please switch into Attachments from an existing Capture.") 
            appuifw.app.activate_tab(3)
            self.butterfly_app.last_index = 3
            self.butterfly_app.capture_app.switch_in()
            return
            
        appuifw.app.title = u'Parent ID: ' + str(self.parent_db['id'])
        appuifw.app.menu = self.butterfly_app.menu_items()
        menu = [(u'Apply Last Picture', self.apply_picture)]
        for x in menu:
            appuifw.app.menu.append(x)
        self.L = [u'Apply Last Picture']
        if 'picture_filename' in self.parent_db:
            if self.parent_db['picture_filename'] is not u'':
                self.L.append(self.parent_db['picture_filename'])
        self.listbox = appuifw.Listbox(self.L,self.listbox_cb)
        appuifw.app.body = self.listbox

    def switch_out(self):
        pass

    def valid_parent_id(self):
        try:
            if self.parent_db['id'] >= 0:
                return 1
        except:
            pass
        return 0
    
    def listbox_cb(self):
        # Later, this callback will need to accommodate
        # different kinds of attachments.
        if self.listbox.current() is 0:
            self.apply_picture()
        else:
            self.view_picture_filename(self.L[self.listbox.current()])

    def apply_picture(self):
        picture_filename = butterfly_helper.get_newest_image_name()
        appuifw.note(u'Applying: ' + picture_filename)
        parent_id = self.parent_db['id']
        captureORM = butterflydb.Captures(self.db, id=parent_id)
        captureORM.set(picture_filename=picture_filename)
        switch_in(captureORM.dict())

    def view_picture_filename(self,picture_filename):
        self.img = Image.new((400,400))
        self.screen_picture = Image.open(picture_filename)
        self.canvas = appuifw.Canvas(redraw_callback=self.handle_redraw)
        self.old_body = appuifw.app.body
        self.old_menu = appuifw.app.menu
        self.old_title = appuifw.app.title
        appuifw.app.title = u'Image'
        appuifw.app.menu = [(u'Back', self.close_picture)]
        appuifw.app.body = self.canvas
        self.handle_redraw(())

    def handle_redraw(self,rect):
        self.img.blit(self.screen_picture,target=(8,10,336,260),scale=1)
        self.canvas.blit(self.img)

    def close_picture(self):
        appuifw.app.body = self.old_body
        appuifw.app.menu = self.old_menu
        appuifw.app.title = self.old_title
