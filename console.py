#!/usr/bin/python

'''
Connectsy console
'''

import os
import sys
from code import InteractiveConsole

#add lib to path
curpath = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(curpath, 'lib')))

if __name__ == '__main__':
    print 'Connectsy REPL'
    print
    
    globals = {}
    locals = {}
    
    repl = InteractiveConsole()
    while True:
        #print '\n> ',
        repl.push(repl.raw_input('>>> '))
        #repl.push(sys.stdin.readline())
    
    print 'Bye'