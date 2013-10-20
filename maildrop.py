#!/usr/bin/env python3
import os
import sys
import maildropper
from subprocess import getoutput

print('qmail env asks for delivery to {0}@{1}\n'.format(os.environ['EXT'],os.environ['HOST']))
homedir=getoutput('vuserinfo -d {0}@{1}'.format(os.environ['EXT'],os.environ['HOST']))
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

