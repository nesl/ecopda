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

butterflydb.TrapsPopulate()

# Read in the DB
db = e32db.Dbms()
db.open(u'e:\\test.db')

positions_db = e32db.Dbms()
# butterflydb.TrapsPopulate needs to be called before the open
positions_db.open(u'e:\\trapsconfig.db')

######################
### Main part of application

def exit_key_handler():
    app_lock.signal()

last_index = 0

def handle_tab(index):
    if index > last_index:
        # Switching right
        if index == 0:
            appuifw.note(u'index cannot be 0',u'alert')
            site_ima_app.switch_in()
        elif index == 1:
            temp_dict = site_ima_app.switch_out()
            xy_position_app.parent_dict = temp_dict
            xy_position_app.switch_in()
        elif index == 2:
            temp_dict = xy_position_app.switch_out()
            trap_app.parent_dict = temp_dict
            trap_app.switch_in()
        elif index == 3:
            temp = trap_app.switch_out()
            capture_app.selection = temp
            capture_app.switch_in()
        elif index == 4:
            temp_dict = capture_app.switch_out()
            attachment_app.parent_dict = temp_dict
            attachment_app.switch_in(temp_dict)
        else:
            appuifw.note(u'Invalid index:' + index, u'alert')
    elif index < last_index:
        # Switching left
        if index == 0:
            xy_position_app.switch_out()
            site_ima_app.switch_in()
            xy_position_app.selection = 0 
        elif index == 1:
            trap_app.switch_out()
            xy_position_app.switch_in()
            trap_app.selection = 0
        elif index == 2:
            capture_app.switch_out()
            trap_app.switch_in()
            capture_app.selection = 0
        elif index == 3:
            attachment_app.switch_out()
            capture_app.switch_in()
    else:
        # Starting up
        site_ima_app.switch_in()
        

# Create an Active object
app_lock = e32.Ao_lock()
# Set exit key handler
appuifw.app.exit_key_handler = exit_key_handler

# Create the tabs with its names in unide as a list, include the tab handler
appuifw.app.set_tabs([u'Site:IMA', u'X,Y:Position', u'Visits',
                      u'Captures', u'Attachments'], handle_tab)
                     

# Create the application objects
capture_app = capture.CaptureApp(db)
trap_app = trap.TrapApp(db)
trap_app.child_db=capture_app
capture_app.parent_db=trap_app.db
site_ima_app = site_ima.SiteImaApp(positions_db)
xy_position_app = xy_position.XYPositionApp(positions_db)
attachment_app = attachment.AttachmentApp(db)
# Set app.body to app1 (for start of script)
handle_tab(0)

app_lock.wait()
