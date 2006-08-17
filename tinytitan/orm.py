from __future__ import generators
import e32db, re

"""
import sys
sys.path.append('e:\\python') # to find sqlshell.py
import orm
import e32db
db = e32db.Dbms()
db.open(u'e:\\test.db') # maybe have to call db.create first

class Person(orm.Mapper):
     class mapping:
         # doesn't need id = column(Integer)
         name = orm.column(orm.String)
         age = orm.column(orm.Integer)

foo = Person.select()
foo.next()


person = Person(db, dbv, id=None, name='Hello',age=5)
"""


# Some helping classes (need more in next version)
class String:
    pass

class Integer:
    pass

class Float:
    pass

class column:
    def __init__(self, coltype):
        self.coltype = coltype


class Mapper(object):
    def __init__(self, db, id=None, **kw):
        self.db = db
        self.dbv = e32db.Db_view()
        if id is None:
            self.id = self._insert(**kw)
        else:
            self.id = id
    def _insert(self, **kw):
        names = ','.join(kw.keys())
        values = ','.join([self.quote(k,v) for k,v in kw.items()])
        tablename = self.__class__.__name__
        q = u"INSERT INTO %s(%s) VALUES (%s)" % (tablename, names, values)
        self.db.execute(q)
        # get last insert ID
        self.dbv.prepare(self.db, u'SELECT id FROM '+tablename+' ORDER BY id DESC')
        self.dbv.first_line()
        self.dbv.get_line()
        return self.dbv.col(1)
    def __getattr__(self, name):
        if name in self.mapping.__dict__:
            q = 'SELECT '+name+' FROM '+self.__class__.__name__
            q += ' WHERE id='+str(self.id)
            self.dbv.prepare(self.db, unicode(q))
            self.dbv.first_line()
            self.dbv.get_line()
            return self.dbv.col(1)
        else:
            return self.__dict__[name]
    def __repr__(self):
        return '<%s id=%d>' % (self.__class__.__name__, self.id)
    def slog_out(self, mydict = None):
        output = ''
        if mydict == None:
            mydict = self.dict()
        for k,v in mydict.items():
            output += '\t\t<field name="'+k+'">'+str(v)+'</field>\n' 
        return output
    def quote(self, name, value):
        if self.mapping.__dict__[name].coltype == String:
            return "'%s'" % value.replace("'", "''")  # encode single quote
        else:
            return str(value)
    def __setattr__(self, name, value):
        if name in self.mapping.__dict__:
            q = 'UPDATE '+self.__class__.__name__+' SET '+name+'='
            q += self.quote(name, value) + " WHERE id=" + str(self.id)
            self.db.execute(unicode(q))
        else:
            self.__dict__[name] = value
    def set(self, **kw):
        q = "UPDATE "+self.__class__.__name__+" SET "
        for k, v in kw.items():
            q += k+'='+self.quote(k,v)+','
        q = q[:-1]+" WHERE id=%s" % self.id
        self.db.execute(unicode(q))
    def delete(self):
        q = 'DELETE FROM '+self.__class__.__name__+" WHERE id=" + str(self.id)
        self.db.execute(unicode(q))
        self.id = None
    def dict(self):
        names = [k for k in self.mapping.__dict__.keys() if not k.startswith('__')]
        q = 'SELECT '+','.join(names)+' FROM '+self.__class__.__name__
        q += ' WHERE id=' + str(self.id)
        self.dbv.prepare(self.db, unicode(q))
        self.dbv.first_line()
        self.dbv.get_line()
        dct = {'id': self.id}
        for i in range(self.dbv.col_count()):
            dct[names[i]] = self.dbv.col(i+1)
        return dct
    # Keep calling next() on the result until you catch a
    # StopIteration Exception 
    def select(cls, db, where=None, orderby=None):
        q = 'SELECT id FROM '+ cls.__name__
        if where:
            q += ' WHERE '+where
        if orderby:
            q += ' ORDER BY '+orderby
        dbv = e32db.Db_view()  # need its own cursor
        dbv.prepare(db, unicode(q))
        dbv.first_line()
        for i in range(dbv.count_line()):
            dbv.get_line()
            yield cls(db, dbv.col(1))
            dbv.next_line()
    select = classmethod(select)

