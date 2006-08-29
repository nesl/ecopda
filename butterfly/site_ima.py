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
    def __init__(self,butterfly_app,db):
        self.butterfly_app = butterfly_app
        self.listbox = None
        self.ListID = []
        self.db = db
        self.dbv = e32db.Db_view()
        self.selected = 0
        
    def switch_in(self):
        appuifw.app.title = u'Site:IMA'
        appuifw.app.menu = []
        L = []
        self.ListID = []
        dict_sites = {} # keeps track of "sites" we've seen. Chris doesn't like this. :P
        trapconfig_iter = TrapsConfig.select(self.db, orderby='id ASC')
        try:
            while 1:
                trapconfigORM = trapconfig_iter.next()
                site_name = unicode(trapconfigORM.site) + ':' + unicode(trapconfigORM.ima)
                if site_name not in dict_sites:
                    L.append(site_name)
                    self.ListID.append(trapconfigORM.id)
                    dict_sites[site_name] = 1
        except StopIteration:
            pass
        self.listbox = appuifw.Listbox(L,self.lb_callback)
        self.listbox.set_list(L, self.selected)
        appuifw.app.body = self.listbox

    def lb_callback(self):
        pass

    def switch_out(self):
        self.selected = self.listbox.current()
        trapsconfigORM = TrapsConfig(self.db,id=self.ListID[self.listbox.current()])
        return trapsconfigORM.dict()
