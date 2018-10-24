#!/usr/bin/env python
'''
Class to manage output, to screen and logfiles.
'''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class messenger:

    def __init__(self,f=None):
        self.f = f

    def setLog(self,f):
        self.f = f

    def error(self,string,log=True):
        msg =  'Error: ' + string
        print(bcolors.FAIL+''+msg+''+bcolors.ENDC)
        if not isinstance(self.f,type(None)):
            self.f.write(msg+'\n')

    def warning(self,string,log=True):
        msg = 'Warning: ' + string
        print(bcolors.WARNING+''+msg+''+bcolors.ENDC)
        if not isinstance(self.f,type(None)):
            self.f.write(msg+'\n')

    def status(self,string,log=False):
        msg = '* ' + string + ' *'
        print(bcolors.OKBLUE+''+msg +''+bcolors.ENDC)
        if not isinstance(self.f,type(None)):
            self.f.write(msg+'\n')

    def info(self,string,log=False):
        msg = '> ' + string
        print(bcolors.OKGREEN+''+msg+''+bcolors.ENDC)
        if not isinstance(self.f,type(None)):
            self.f.write(msg+'\n')

    def say(self,string,log=False):
        msg = string
        print(msg)
        if not isinstance(self.f,type(None)) and log:
            self.f.write(msg+'\n')
