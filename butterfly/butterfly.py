import appuifw
import e32
import time

import sys
sys.path.append('e:\\python') #to properly find orm and keyboard
import orm
import keyboard
import capture
import trap
import site_ima
import xy_position
import e32db
import butterflydb
import attachment

# Create the application objects
class ButterflyApp:
    def __init__(self):
        # butterflydb.TrapsPopulate needs to be called before the open
        butterflydb.TrapsPopulate()
        # Read in the DB
        self.db = e32db.Dbms()
        self.db.open(u'e:\\test.db')
        self.positions_db = e32db.Dbms()
        self.positions_db.open(u'e:\\trapsconfig.db')
        self.last_index = 0
        self.capture_app = capture.CaptureApp(self, self.db)
        self.trap_app = trap.TrapApp(self, self.db)
        self.trap_app.child_db = self.capture_app
        self.capture_app.parent_db = self.trap_app.db
        self.site_ima_app = site_ima.SiteImaApp(self, self.positions_db)
        self.xy_position_app = xy_position.XYPositionApp(self, self.positions_db)
        self.attachment_app = attachment.AttachmentApp(self, self.db)
        self.app_lock = e32.Ao_lock()
        # Set exit key handler
        appuifw.app.exit_key_handler = self.exit_key_handler
        # Create the tabs
        appuifw.app.set_tabs([u'Site:IMA', u'X,Y:Position', u'Visits',
                              u'Captures', u'Attachments'], self.handle_tab)
        # Set app.body to app1 (for start of script)
        self.handle_tab(0)

    def exit_key_handler(self):
        self.app_lock.signal()

    def handle_tab(self, index):
        if index > self.last_index:
            # Switching right
            if index == 0:
                appuifw.note(u'index cannot be 0',u'alert')
                self.site_ima_app.switch_in()
            elif index == 1:
                temp_dict = self.site_ima_app.switch_out()
                self.xy_position_app.parent_dict = temp_dict
                self.xy_position_app.switch_in()
            elif index == 2:
                temp_dict = self.xy_position_app.switch_out()
                self.trap_app.parent_dict = temp_dict
                self.trap_app.switch_in()
            elif index == 3:
                temp = self.trap_app.switch_out()
                self.capture_app.selection = temp
                self.capture_app.switch_in()
            elif index == 4:
                temp_dict = self.capture_app.switch_out()
                self.attachment_app.parent_dict = temp_dict
                self.attachment_app.switch_in(temp_dict)
            else:
                appuifw.note(u'Invalid index:' + index, u'alert')
        elif index < self.last_index:
            # Switching left
            if index == 0:
                self.xy_position_app.switch_out()
                self.site_ima_app.switch_in()
                self.xy_position_app.selection = 0 
            elif index == 1:
                self.trap_app.switch_out()
                self.xy_position_app.switch_in()
                self.trap_app.selection = 0
            elif index == 2:
                self.capture_app.switch_out()
                self.trap_app.switch_in()
                self.capture_app.selection = 0
            elif index == 3:
                self.attachment_app.switch_out()
                self.capture_app.switch_in()
        else:
            # Starting up
            self.site_ima_app.switch_in()

butterfly_app = ButterflyApp()
butterfly_app.app_lock.wait()
