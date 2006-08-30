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
    def __init__(self,butterfly_app,db):
        self.butterfly_app = butterfly_app
        self.listbox = None
        self.ListID = []
        self.db = db
        self.dbv = e32db.Db_view()
        self.selected = 0
        self.parent_dict = {}
        
    def switch_in(self):
        appuifw.app.title = unicode(self.parent_dict['site'] + ':' + str(self.parent_dict['ima']) + u':(X,Y):Position' )
        appuifw.app.menu = self.butterfly_app.menu_items()
        appuifw.app.menu.append((u'Barcode View', self.barcode_view))
        L = []
        self.ListID = []
        where_query = u"(site = '" + self.parent_dict['site'] 
        where_query += "\' AND ima=" + str(self.parent_dict['ima']) + ')'
        trapconfig_iter = TrapsConfig.select(self.db, where=where_query ,orderby='id')
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
        trapconfigORM = TrapsConfig(self.db,id=self.ListID[self.listbox.current()])
        appuifw.popup_menu([unicode(trapconfigORM.barcode)],u'Barcode')

    def switch_out(self):
        trapsconfigORM = TrapsConfig(self.db,id=self.ListID[self.listbox.current()])
        return trapsconfigORM.dict()

    def barcode_view(self):
        trapconfigORM = TrapsConfig(self.db,id=self.ListID[self.listbox.current()])
        appuifw.popup_menu([unicode(trapconfigORM.barcode)],u'Barcode')
        
