#!/usr/bin/python

class Member():
    '''
    m1 = Member()
    m2 = Member()
    m1.Membernum
    4
    m2.Membernum
    4
    m2.Membernum=6
    m1.Membernum
    4
    '''
    Membernum = 0
    def __init__(self):
        Member.Membernum += 1

class superclass():
    def __init__(self):
        self.blockerd = []
    def filter(self,seqence):
        return [x for x in seqence if x not in self.blockerd]

class sunclass(superclass):
    def __init__(self):
        self.blockerd = ['a']

issubclass(sunclass,superclass)  #True
isinstance(s,superclass) #True
#sunclass.__bases__ (<class __builtin__.superclass at 0x101771530>,)
#s.__class__


class Calculator():
    def calculator(self,expression):
        self.value = eval(expression)

class Talk():
    def talk(self):
        print "Hi,value is %s" % self.value



class TalkCalculator(Calculator,Talk):
    pass

a = TalkCalculator()
a.calculator('1+4')
a.talk()
callable(getattr(a,'talk',None))
hasattr(a,'talk')
setattr(a,'name',"Leo")


#New type class,use supper

__metaclass__ = type

class Bird:
    def __init__(self,wight=0,hight=0):
        self.hangry = True
        self.wight = wight
        self.hight = hight
    def eat(self):
        if self.hangry:
            print("Aaaaah...")
            self.hangry = False
        else:
            print("No...")
    def setsize(self,size):
        self.wight, self.hight = size
    def getsize(self):
        print (self.wight, self.hight)
    size = property(getsize, setsize)


class SoundBird(Bird):
    def __init__(self):
        super(SoundBird, self).__init__()
        self.sound = "Squawk!!!"
    def sing(self):
        print(self.sound)



