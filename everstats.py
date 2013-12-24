#!/usr/bin/env python

"""
A project to plot my Evernote stats.
For example:
- view notes tagged "feminist" according to time stored


Input
Asks for a word or search phrase to filter notes with
Should ask for the DEV_TOKEN, but only once at the beginning

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
- Feroz says it would be more useful to look at weeks (but hard to do > could do it with the .weekday method) 
    - I think months could already be interesting
    - could be interesting to see if I read these articles at a particular day or time in the week or even day


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

from itertools import chain

from code import interact
# interact(local=locals())

DEV_TOKEN = open("token.txt").read()

def connect2Ev(check=False):
    client = EvernoteClient(token=DEV_TOKEN, sandbox=False)
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
    list_tags = noteStore.listTags(DEV_TOKEN)

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
    total_num_notes = found_notes.totalNotes
    found_notes = found_notes.notes

    while len(found_notes) < total_num_notes:
        new_found_notes = noteStore.findNotesMetadata(note_filter, len(found_notes), 10000, resultSpec).notes
        found_notes = list(chain.from_iterable([new_found_notes, found_notes]))
        
    if verbose:
        print "Total amount of notes tagged with '%s': %d" % (note_filter.words, len(found_notes))
    return found_notes


def makeData(list_notes, by_month):
    """
    
    """
    notes = sorted(list_notes, key=lambda n: n.created)

    dates = []
    content = []
    # convert all epoch timestaps to just dates
    for i, note in enumerate(notes):

        epoch_date_created = float(note.created)/1000.
        date_created = dt.datetime.fromtimestamp(epoch_date_created)
        date_created = date_created.date()
        if by_month:
            date_created = date_created.replace(day=1)
        dates.append(date_created)

        content.append(note.contentLength)

    notes = zip(dates, content)


    dates = [notes[0][0]]
    content = [notes[0][1]]
    num_notes = [1]

    i = 0

    for note in notes:

        note_date = note[0]

        if note_date == dates[i]:
            content[i] += note[1]
            num_notes[i] += 1
        else:
            dates.append(note_date)
            content.append(note[1])
            num_notes.append(1)
            i += 1

    return (dates, num_notes, content)


def makePlot(data, by_month, show=True):
    """
    x:  date info
    y1: number of notes with the search_term
    y2: total content of the notes with the search_term

    """
    if by_month:
        width = 31
    else:
        width = 1

    x, y1, y2 = data

    ax = plt.gca()
    ax2 = ax.twinx()
    ax.bar( x, y1, align="center", facecolor='#9999ff', lw=0, width=width)   # number notes in blue
    ax2.bar(x, y2, align="center", facecolor='#ff9999', lw=0, width=width)   # content in red
    if show:
        plt.show()
    # save plot
    return


def main(search_term, search_by, by_month=True):

    noteStore = connect2Ev()

    if search_by == "tag":
        nFilter = NoteStoreTypes.NoteFilter(tagGuids=findTagGuids(noteStore, search_term))

    elif search_by == "word":
        nFilter = NoteStoreTypes.NoteFilter(words=search_term)
    
    notes = findNotes(noteStore, nFilter, True)

    data = makeData(notes, by_month=by_month)
    makePlot(data, by_month=by_month, show=True)

    return


if __name__ == '__main__':

    sys.exit(main(sys.argv[2], sys.argv[1], False))

