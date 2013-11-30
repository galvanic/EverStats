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

def filterByTag(tagname, wordy=False):
    """
    Returns a list of tag GUIDS corresponding to tag names inputed (string).
    Only returns one tag for the moment, might make it do more later.
    """
    list_tags = noteStore.listTags(dev_token)

    for t in list_tags:
        if tagname in t.name.lower():
            if wordy:
                print "Found tag %s" % t.name
            wanted_tag = t.guid
            break
    else:
        print "No tag with '%s' in its name was found." % tagname
    return [wanted_tag]


fem_filter = NoteStoreTypes.NoteFilter(tagGuids=filterByTag("feminis"))
fem_notes  = noteStore.findNoteCounts(dev_token, fem_filter, False)

total_fem = sum(fem_notes.notebookCounts.values())
print total_fem


# But that's not what I was looking for :(
# I want to find the actual notes with this tag, so that I can get their createdDate and plot them












