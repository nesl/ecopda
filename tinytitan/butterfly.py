import appuifw
import e32
import time

import sys
sys.path.append('e:\\python') #to properly find orm and keyboard
import orm
import keyboard
import capture

import e32db

# Read in the DB
db = e32db.Dbms()
db.open(u'e:\\test.db')

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

# Create the tabs with its names in unide as a list, include the tab handler
appuifw.app.set_tabs([u'Capture'], handle_tab)

# Create the application objects
capture_app = capture.CaptureApp(db)

# Set app.body to app1 (for start of script)
handle_tab(0)

app_lock.wait()
