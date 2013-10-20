#!/usr/bin/env python
import sys
import os
import email
import email.parser
import datetime
import mailbox

class Maildropper(object):
    '''
    Wrapper for mailbox and email to receive qmail input and drop in a qmail maildir
    '''
    logfile = None
    msg = None
    msg_id = None
    dry_run = None
    home=None
    mdir=None

    def __init__(self, folder=None,logfile=None, dry_run=False):
        if logfile is not None:
            self.logfile = open(logfile, 'a+')
        else:
            self.logfile = sys.stdout

        #set our home directory
        if folder is None:
            self.home='./.maildir'
        else:
            self.home=folder

        self.mdir=mailbox.Maildir(self.home)
        
        self.msg = email.parser.BytesParser().parse(sys.stdin.buffer)
        self.dry_run = dry_run
            
        self.now = now = datetime.datetime.now()
        self.msg_id = self.msg['X-Maildrop-Id'] = str(hash(now))
        self.headers=dict(zip(self.msg.keys(), self.msg.values()))

        if "Date" in self.headers and "From" in self.headers and "To" in self.headers and "Subject" in self.headers:
            self.log('Date: {0}\nFrom: {1}\nTo: {2}\nSubject: {3}\n'.format(self.headers['Date'],self.headers['From'],self.headers['To'],self.headers['Subject']))
        else: 
            self.log('missing some headers {0}\n'.format(self.headers))
        
    def drop(self,folder=None):
        
        if folder is None: 
            self.log(' ===> Writing to {0}\n'.format(self.home))
            self.mdir.add(self.msg)
        elif folder not in self.mdir.list_folders():
            self.mdir.add(self.msg)
            self.log(' ===> Requested drop point {0} not found\n'.format(folder))
            self.log(' ===> Writing to {0}\n'.format(self.home))
        else:
            self.log(' ===> Writing to {0}\n'.format(folder))
            self.mdir.get_folder(folder).add(self.msg)
        
        
   
    def log(self, msg):
        if '\n' in msg:
            for sub in msg.split('\n'):
                self.log(sub)
        elif '\r' in msg:
            for sub in msg.split('\r'):
                self.log(sub)
        else:
            self.logfile.write('{0} {1}\n'.format(self.now,msg))

    def header(self, name):
        return str(self.msg.get(name, ''))
