#!/usr/bin/env python

"""
A project to plot my evernote stats.
For example:
- view notes tagged "feminist" according to time stored


"""

import evernote.edam.notestore.ttypes as NoteStoreTypes

from evernote.api.client import EvernoteClient


dev_token = "S=s4:U=a2310:E=14a00ca558f:C=142a9192994:P=1cd:A=en-devtoken:V=2:H=e95b413c4a9edd294396ba799b600082"
client = EvernoteClient(token=dev_token, sandbox=False)
userStore = client.get_user_store()
user = userStore.getUser()
print user.username

noteStore = client.get_note_store()

# notebooks = noteStore.listNotebooks()
# for n in notebooks:
#     print n.name

# ###
# nFilter = NoteStoreTypes.NoteFilter()
# nFilter.words = getNonEmptyUserInput("Search for: ")
# resultSpec = NoteStoreTypes.NotesMetadataResultSpec()
# resultSpec.includeTitle = True

# searchResults = note_store.findNotesMetadata(nFilter, 0, 10, resultSpec)

# if len(searchResults.notes):
#     for note in searchResults.notes:
#         print note.guid
#         print note.title
# else:
#     print "No results, big fella."
###

# get the guid of the tag we are looking for by searching for its name through a tag list
list_tags = noteStore.listTags(dev_token)
search_tag = "feminis"

for i, t in enumerate(list_tags):
    if search_tag in t.name.lower():
        print "Found tag %s" % t.name
        fem_guid = t.guid
        break
else:
    print "No tag with '%s' in its name was found." % search_tag

fem_filter = NoteStoreTypes.NoteFilter(tagGuids=[fem_guid])
fem_notes  = noteStore.findNoteCounts(dev_token, fem_filter, False)

total_fem = sum(fem_notes.notebookCounts.values())
print total_fem



