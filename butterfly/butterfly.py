import appuifw
import e32

t = appuifw.Text()
appuifw.body = t
t.clear()
t.add(u'Loading...')


import e32db
import sys
sys.path.append('e:\\python') #to properly find orm and keyboard
import butterflydb
import capture
import trap,site_ima,xy_position,attachment
import thread

def importRest():
    time, orm, keyboard,socket,string = \
    [ \
        __import__('time'),
        __import__('orm'),
        __import__('keyboard'),
        __import__('socket'),
        __import__('string')]
thread.start_new_thread(importRest,())

# Create the application objects 
class ButterflyApp:
    def __init__(self):
        # Database stuff start
        trapsconfigdb = u'e:\\trapsconfig.db'
        testdb = u'e:\\test.db'
        self.db = e32db.Dbms()
        try:
            self.db.open(testdb)
        except:
            self.db.create(testdb)
            self.db.open(testdb)

        try:
            butterflydb.Captures.create_table(self.db);
        except:
            pass
        try:
            butterflydb.Traps.create_table(self.db);
        except:
            pass
        butterflydb.TrapsPopulate() # populates trapsconfig.{db,txt}
        self.positions_db = e32db.Dbms()
        self.positions_db.open(trapsconfigdb)
        # Databse stuff end
        
        self.last_index = 0
        self.capture_app = capture.CaptureApp(self, self.db)
        self.trap_app = trap.TrapApp(self, self.db)
        self.trap_app.child_db = self.capture_app
        self.capture_app.parent_db = self.trap_app.db
        self.site_ima_app = site_ima.SiteImaApp(self, self.positions_db)
        self.xy_position_app = xy_position.XYPositionApp(self, self.positions_db)
        self.attachment_app = attachment.AttachmentApp(self, self.db)
        self.app_lock = e32.Ao_lock()
        self.short_cut = 0
        # Set exit key handler
        appuifw.app.exit_key_handler = self.exit_key_handler
        # Create the tabs
        appuifw.app.set_tabs([u'Site:IMA', u'X,Y:Position', u'Visits',
                              u'Captures', u'Attachments'], self.handle_tab)
        # Set app.body to app1 (for start of script)
        self.handle_tab(0)
        self.user = u'None'
        
        
    def exit_key_handler(self):
        self.app_lock.signal()

    def handle_tab(self, index):
#         if self.short_cut:
#             self.short_cut = 0
#             if index == 2:
#                 self.capture_app.switch_in()
#             else:
#                 appuifw.note(u"I don't know that shortcut")
        # I have to use a tmp variable because there are situations
        # where an app's switch_in wants to modify self.last_index
        # during its execution.
        tmp_last_index = self.last_index
        self.last_index = index
        if index > tmp_last_index:
            # Switching right
            if index == 0: # Site:IMA
                appuifw.note(u'index cannot be 0',u'alert')
                self.site_ima_app.switch_in()
            elif index == 1: # XY:Pos
                temp_dict = self.site_ima_app.switch_out()
                self.xy_position_app.parent_dict = temp_dict
                self.xy_position_app.switch_in()
            elif index == 2: # Visits
                temp_dict = self.xy_position_app.switch_out()
                self.trap_app.parent_dict = temp_dict
                self.trap_app.switch_in()
            elif index == 3: # Captures
                temp_dict = self.trap_app.switch_out()
                self.capture_app.parent_dict = temp_dict
                self.capture_app.switch_in()
            elif index == 4: # Attachments
                temp_dict = self.capture_app.switch_out()
                self.attachment_app.switch_in(temp_dict)
            else:
                appuifw.note(u'Invalid index:' + index, u'alert')
        elif index < tmp_last_index:

            # Switching left
            if index == 0: # Site:IMA
                self.xy_position_app.switch_out()
                self.site_ima_app.switch_in()
                self.xy_position_app.selection = 0 
            elif index == 1: # XY:Pos
                self.trap_app.switch_out()
                self.xy_position_app.switch_in()
                self.trap_app.selection = 0
            elif index == 2: # Visits
                self.capture_app.switch_out()
                self.trap_app.switch_in()
                self.capture_app.selection = 0
            elif index == 3: # Captures
                self.attachment_app.switch_out()
                self.capture_app.switch_in()
        else:
            # Either we're starting up, or something is
            # messed up.
            self.site_ima_app.switch_in()

        
    # menu should be appuifw.app.menu or equivalent
    def menu_items(self):
        return [(u'Barcode Jump', self.barcode_jump),
                (u'Barcode Launch', self.barcode_start),
                (u'Set User', self.set_user)]

    def set_user(self):
        save_user=appuifw.query(u'Enter user name:', 'text', self.user)
        if not save_user:
            return
        else:
            self.user = unicode(save_user)
            appuifw.note(u'You entered: '+self.user)

    def barcode_start(self):
        host = '127.0.0.1'
        port = 88
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        s.close()

    def stupid(self, barcode_result):
        result = ""
        for e in barcode_result:
            if e != '\x00':
                result += e
        return result

    def barcode_read(self):
        barcodefile = u'e:\\mylog.txt'
        barcode_result = None
        try:
            f = open(barcodefile)
        except:
            appuifw.note(u'Unable to read barcode file')
            return u''
        try:
            barcode_result = self.stupid(f.read())
#            appuifw.note(u'barcode: ' + barcode_result)
        except:
            appuifw.note(u'unable to read: ' + barcodefile)
        f.close()
        return barcode_result

    def barcode_jump(self):
        barcode_result = self.barcode_read()
        #TODO: set "history" for the trap_app's parents
        
        #Look up in the traps DB
        #  (barcode = '132131241')
        where_query = u"(barcode = '" + barcode_result + "')"

        #Get corresponding trapORM
        try:
            trapconfig_iter = butterflydb.TrapsConfig.select(self.positions_db,where=where_query, orderby='id')
        except SymbianError:
            appuifw.note(u'Error with query', u'error')
        try:
            trapconfigORM = trapconfig_iter.next()
            self.trap_app.parent_dict = trapconfigORM.dict()
            appuifw.app.activate_tab(2)
            self.last_index = 2
            self.trap_app.switch_in()
        except (StopIteration, SymbianError):
            appuifw.note(u'Unable to find matching trap.', u'error')


butterfly_app = ButterflyApp()
butterfly_app.app_lock.wait()
