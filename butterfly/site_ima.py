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

class SiteImaApp:
    def __init__(self,db):
        self.listbox = None
        self.ListID = []
        self.db = db
        self.dbv = e32db.Db_view()
        self.selected = 0
        
    def switch_in(self):
        appuifw.app.title = u'Site/IMA'
        appuifw.app.menu = []
        L = []
        self.ListID = []
        trapconfig_iter = TrapsConfig.select(self.db, orderby='id DESC')
        try:
            while 1:
                trapconfigORM = trapconfig_iter.next()
                L.append(unicode(trapconfigORM.site)
                         + ':' + unicode(trapconfigORM.ima))
                self.ListID.append(trapconfigORM.id)
        except StopIteration:
            pass
        self.listbox = appuifw.Listbox(L,self.lb_callback)
        appuifw.app.body = self.listbox

    def lb_callback(self):
        pass

    def switch_out(self):
        self.selected = self.listbox.current()
        trapsconfigORM = TrapsConfig(self.db,id=self.ListID[self.listbox.current()])
        return trapsconfigORM.dict()
