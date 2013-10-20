#!/usr/bin/env python3
import os
import sys
import maildropper
from subprocess import getoutput

deliverytarget='{0}@{1}'.format(os.environ['EXT'],os.environ['HOST'])
print('qmail env asks for delivery to {0}\n'.format(deliverytarget))

#alias?
#check for valias output: alas@somedomain.com -> realacct@otherdomain.com
alias=getoutput('/var/vpopmail/bin/valias {0}'.format(deliverytarget))
if len(alias):
    deliverytarget=alias.split('->')[1].strip()

#get homedir/check valid user    
homedir=getoutput('/var/vpopmail/bin/vuserinfo -d {0}'.format(deliverytarget))
if 'no such user' in homedir:
    print('exiting..no such user')
    sys.exit(1)

homedir=homedir+'/.maildir'
print("Homedir is " +homedir)

#init maildropper (sucks in stdin)
m = maildropper.Maildropper(folder=homedir)

#anything printed here returns to qmail and is logged
print(m.home)
#print('Sender:{0}'.format(m.headers['Sender']))
#print('Date:{0}'.format(m.headers['Received']))
if 'Subject' in m.headers:
    if m.headers['Subject'].startswith('[SPAM]'):
        m.drop('spam')
    else:
        m.drop()
else:    
    m.drop()

