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

class XYPositionApp:
    def __init__(self,db):
        self.listbox = None
        self.ListID = []
        self.db = db
        self.dbv = e32db.Db_view()
        self.selected = 0
        self.parent_dict = {}
        
    def switch_in(self):
        appuifw.app.title = unicode(self.parent_dict['site'] + ':' + str(self.parent_dict['ima']))
        appuifw.app.menu = []
        L = []
        self.ListID = []
        where_query = u"(site = '" + self.parent_dict['site'] 
        where_query += "\' AND ima=" + str(self.parent_dict['ima']) + ')'
        trapconfig_iter = TrapsConfig.select(self.db, where=where_query ,orderby='id DESC')
        try:
            while 1:
                trapconfigORM = trapconfig_iter.next()
                L.append(u'(' + unicode(trapconfigORM.xcoord)
                         + ',' + unicode(trapconfigORM.ycoord)
                         + '):' + unicode(trapconfigORM.position))
                self.ListID.append(trapconfigORM.id)
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
