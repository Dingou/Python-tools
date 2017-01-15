# getattr
# Return the value of the named attribute of object. name must be a string. If the string is the name of one of the object's attributes, the result is the value of that attribute. For example, getattr(x, 'foobar') is equivalent to x.foobar. If the named attribute does not exist, default is returned if provided, otherwise AttributeError is raised.
#在 Python 中，当访问一个对象的会根据不同的情况作不同的处理，是比较复杂的。一般象a.b这样的形式，
#python可能会先查找a.__dict__中是否存在，如果不存在会在类的__dict__中去查找，再没找到可能会去按这种方法去父类中进行查找。
#实在是找不到，会调用__getattr__，如果不存在则返回一个异常。那么__getattr__只有当找不到某个属性的时候才会被调用。
#因此，你可能会想实现一种机制，当访问一个不存的属性时，自动提供一个缺省值，这样不是挺好，而且 NewEdit 中已经这样做了。
#但在邮件列表中Carlos报告说 NewEdit 运行不了。今天我偶然装回了wxPython 2.4.2.4，发现这个问题的确是存在的，
#但在wxPython 2.5以上好象没出过，很奇怪。问题基本上是这样的：


class chain(object):
    def __init__(self,path=''):
        self._path = path

    def __getattr__(self, path):
        return chain("%s/%s" % (self._path,path))

    def __str__(self):
        return self._path

    __repr__ = __str__