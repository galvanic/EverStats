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
    - plot logarithmically ?
    - plot by "feminist activity" (so a yes/no of whether there are fem posts that day) with varying colours for strength ?
- include a wider range of notes (some feminist notes aren't tagged yet)


Bugs
- wtf 22/07/2013 ?? ah, sinfest => how to deal with outliers ?
- images can completely skew the contentLength :-|
    - maybe count all images the same number of "content" ?
    - sometimes images aren't downloaded in the note (eg. sinfest)


What else could I look at ? What can my Evernote usage tell me ?

"""

import sys

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
        print "Total amount of notes tagged with '%s': %d" % (note_filter.words, found_notes.totalNotes)
    return found_notes


def makeData(list_notes):
    """"""
    notes = sorted(list_notes.notes, key=lambda n: n.created)

    dates = []
    content = []
    # convert all epoch timestaps to just dates
    for note in notes:

        epoch_date_created = float(note.created)/1000.
        date_created = dt.datetime.fromtimestamp(epoch_date_created)
        date_created = date_created.date()
        dates.append(date_created)

        content.append(note.contentLength)

    notes = zip(dates, content)


    dates = [notes[0][0]]
    content = [notes[0][1]]
    num_notes = [1]

    i = 0

    for note in notes:

        if note[0] == dates[i]:
            content[i] += note[1]
            num_notes[i] += 1
        else:
            dates.append(note[0])
            content.append(note[1])
            num_notes.append(1)
            i += 1

    # arg that felt a bit finicky

    return (dates, num_notes, content)


def makePlot(data):
    """"""
    x, y1, y2 = data
    ax = plt.gca()
    ax2 = ax.twinx()
    ax.bar( x, y1, align="center", facecolor='#9999ff', lw=0)
    ax2.bar(x, y2, align="center", facecolor='#ff9999', lw=0)
    plt.show()


def main(search_term, search_by="word"):

    noteStore = connect2Ev()

    if search_by == "tag":
        nFilter = NoteStoreTypes.NoteFilter(tagGuids=findTagGuids(search_term))

    elif search_by == "word":
        nFilter = NoteStoreTypes.NoteFilter(words=search_term)
    
    notes = findNotes(noteStore, nFilter, True)

    data = makeData(notes)
    makePlot(data)

    return


if __name__ == '__main__':

    # main()
    sys.exit(main(sys.argv[1]))

