#!/usr/bin/env python3
import os
import sys
import maildropper
from subprocess import check_output
from subprocess import CalledProcessError

deliverytarget='{0}@{1}'.format(os.environ['EXT'],os.environ['HOST'])
print('qmail env asks for delivery to {0}\n'.format(deliverytarget))

#alias?
#check for valias output: alas@somedomain.com -> realacct@otherdomain.com
try:
    alias=check_output(['/var/vpopmail/bin/valias',deliverytarget],shell=False)
    if len(alias):
        deliverytarget=alias.decode('ascii','ignore').strip().split('->')[1].strip()
except CalledProcessError:
    #no alias
    pass

#get homedir/check valid user
try:
    homedir=check_output(['/var/vpopmail/bin/vuserinfo','-d',deliverytarget],shell=False)
except CalledProcessError:
    print('exiting..no such user')
    sys.exit(1)

homedir=homedir.decode('ascii','ignore').strip()+'/.maildir'
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

