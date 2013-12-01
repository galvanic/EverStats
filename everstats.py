#!/usr/bin/env python

"""
A project to plot my Evernote stats.
For example:
- view notes tagged "feminist" according to time stored


"""

import evernote.edam.notestore.ttypes as NoteStoreTypes
from evernote.api.client import EvernoteClient

import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from code import interact
# interact(local=locals())


dev_token = "S=s4:U=a2310:E=14a00ca558f:C=142a9192994:P=1cd:A=en-devtoken:V=2:H=e95b413c4a9edd294396ba799b600082"
client = EvernoteClient(token=dev_token, sandbox=False)
userStore = client.get_user_store()
user = userStore.getUser()
print "Connected to user account %s" % user.username

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
# ###

def filterByTag(tagname, verbose=False):
    """
    Returns a list of tag GUIDS corresponding to tag names inputed (string).
    Only returns one tag for the moment, might make it do more later.
    """
    list_tags = noteStore.listTags(dev_token)

    for t in list_tags:
        if tagname in t.name.lower():
            if verbose:
                print "Found tag %s" % t.name
            wanted_tag = t.guid
            break
    else:
        print "No tag with '%s' in its name was found." % tagname
    return [wanted_tag]


nFilter = NoteStoreTypes.NoteFilter(tagGuids=filterByTag("feminis"))
# fem_notes = noteStore.findNoteCounts(dev_token, fem_filter, False)

# total_fem = sum(fem_notes.notebookCounts.values())
# print total_fem


# But that's not what I was looking for :(
# I want to find the actual notes with this tag, so that I can get their createdDate and plot them

resultSpec = NoteStoreTypes.NotesMetadataResultSpec(
    includeTitle = True,
    includeContentLength = True,
    includeCreated = True,
    includeUpdated = False,
    includeDeleted = False,
    includeUpdateSequenceNum = False,
    includeNotebookGuid = False,
    includeTagGuids = False,
    includeAttributes = False,
    includeLargestResourceMime = False,
    includeLargestResourceSize = False,
    )
list_femnotes = noteStore.findNotesMetadata(nFilter, 0, 10000, resultSpec)
print "Total amount of feminist tagged notes: %d" % list_femnotes.totalNotes


dates = []
content = []
for note in list_femnotes.notes:

    # data for the x axis: date note was created
    epoch_date_created = float(note.created)/1000.
    date_created = dt.datetime.fromtimestamp(epoch_date_created)
    date_created = date_created.date()
    dates.append(date_created)

    # data for the y axis: total note content length for that day
    content.append(note.contentLength)

# zip it up
fem_notes = zip(dates, content)
# sort by date if it isn't already
fem_notes = sorted(fem_notes, key=lambda n: n[0])
# go through and add if same date (arg must be a more efficient way of doing this !) => maybe sort them beforehand ?
dates = [fem_notes[0][0]]
content = [fem_notes[0][1]]
num_notes = [1]
i = 0
for femn in fem_notes:
    if femn[0] == dates[i]:
        content[i] += femn[1]
        num_notes[i] += 1
    else:
        dates.append(femn[0])
        content.append(femn[1])
        num_notes.append(1)
        i += 1
# arg that felt a bit finicky


# make the plot
x = dates
y = num_notes
plt.bar(x, y)
plt.show()












