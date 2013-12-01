#!/usr/bin/env python

"""
A project to plot my Evernote stats.
For example:
- view notes tagged "feminist" according to time stored


Input
Nothing for the moment, but should be the dev_token
Maybe the tag/word searched for ?

Output
Plot of notes with that tag against time


Improvements
- black box everything into functions
- make plot prettier
    - my own tweaks
    - look at other libraries
- compare two measures for the same day: amount of notes, and total content length of those notes put together
- find a way to deal with outliers (both horizontal, in time, and vertical, spike of reading in a day)
- include a wider range of notes (some feminist notes aren't tagged yet)


Bugs
- wtf 22/07/2013 ?? ah, sinfest => how to deal with outliers ?
- images can completely skew the contentLength :-|
    - maybe count all images the same number of "content" ?
    - sometimes images aren't downloaded in the note (eg. sinfest)


What else could I look at ? What can my Evernote usage tell me ?

"""

import evernote.edam.notestore.ttypes as NoteStoreTypes
from evernote.api.client import EvernoteClient

import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from code import interact
# interact(local=locals())


def connect2Ev(check=False):
    dev_token = "S=s4:U=a2310:E=14a00ca558f:C=142a9192994:P=1cd:A=en-devtoken:V=2:H=e95b413c4a9edd294396ba799b600082"
    client = EvernoteClient(token=dev_token, sandbox=False)
    if check:
        userStore = client.get_user_store()
        user = userStore.getUser()
        print "Connected to user account %s" % user.username
    noteStore = client.get_note_store()
    return noteStore


def findTagGuids(noteStore, tagname, verbose=False):
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


def findNotes(noteStore, note_filter, verbose=False):
    """"""
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
    found_notes = noteStore.findNotesMetadata(note_filter, 0, 10000, resultSpec)
    if verbose:
        print "Total amount of feminist tagged notes: %d" % found_notes.totalNotes
    return found_notes


def sortNotes(list_notes):
    """"""
    dates = []
    content = []
    for note in list_notes.notes:

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
    return (dates, num_notes, content)


def makePlot(data):
    """"""
    x, y1, y2 = data
    plt.subplot(2,1,1)
    plt.bar(x, y1, align="center")
    plt.subplot(2,1,2)
    plt.bar(x, y2, align="center")
    plt.show()


def main():

    noteStore = connect2Ev()

    # nFilter = NoteStoreTypes.NoteFilter(tagGuids=findTagGuids("feminis"))
    nFilter = NoteStoreTypes.NoteFilter(words="feminism")
    notes = findNotes(noteStore, nFilter)

    data = sortNotes(notes)
    makePlot(data)

    return


if __name__ == '__main__':

    main()
    # sys.exit(main(sys.argv[1]))








