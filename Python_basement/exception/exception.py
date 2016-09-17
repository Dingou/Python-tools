#!/usr/bin/python

import exceptions
import sys
import warnings


class MuffledCalculator():
    Mullfed = False
    def calc(self,expr):
        try:
            return eval(expr)
        except ZeroDivisionError:
            if self.Mullfed:
                print "Division should not be zero!"
            else:
                raise

    def exception_ex1(self):
        try:
            x = input("Number one:")
            y = input("Number two:")
            print x / y
        except ZeroDivisionError:
            print "y should not be zero!"
        except TypeError:
            print "y should be a number!"
        except Exception as e:    #every exception could make an Exception as e.it will catch every exception
            print "Invalid input:",e
            print "Try again"
        finally:
            print "Now finish"
        '''
        knowledge:
        1. except (ZeroDivisionError, TypeError, NameError) as e:
              print e
        2. if "expect:" It will catch every exception,but we suggest using "except Exception,e:"
        3. use  "try:  except:  else:break  only break when no exception occurs"
        4.
        '''

    def raisexception(self):
        raise Exception("Something is wrong")

    def ignore_exception(self):
        self.raisexception()



if __name__ == "__main__":
    calculator = MuffledCalculator()
    calculator.exception_ex1("10/2")
    calculator.ignore_exception()
    warnings.filterwarnings()  #filter warnings


#TBC

