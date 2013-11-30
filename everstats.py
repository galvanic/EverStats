#!/usr/bin/env python

"""
A project to plot my evernote stats.
For example:
- view notes tagged "feminist" according to time stored


"""

from evernote.api.client import EvernoteClient


dev_token = "S=s4:U=a2310:E=14a00ca558f:C=142a9192994:P=1cd:A=en-devtoken:V=2:H=e95b413c4a9edd294396ba799b600082"
client = EvernoteClient(token=dev_token, sandbox=False)
userStore = client.get_user_store()
user = userStore.getUser()
print user.username

noteStore = client.get_note_store()
notebooks = noteStore.listNotebooks()
for n in notebooks:
    print n.name, len(n)

