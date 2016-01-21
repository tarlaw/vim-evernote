import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.limits.constants as Limits
import evernote.edam.type.ttypes as Types
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient

from config import *

#
def getNoteStore():

    noteStoreHttpClient = THttpClient.THttpClient(noteStoreUrl)
    noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
    noteStore = NoteStore.Client(noteStoreProtocol)

    return noteStore

#
noteStore = getNoteStore()

#
def EvernoteCreateNewNote(note):
    return noteStore.createNote(authToken, note)

#
def EvernoteCreateNewNotebook(notebook):
    return noteStore.createNotebook(authToken, notebook)

#
def EvernoteFindNoteCounts():
    return noteStore.findNoteCounts(authToken, NoteStore.NoteFilter(), False)

#
def EvernoteGetDefaultNotebook():
    return noteStore.getDefaultNotebook(authToken)

#
def EvernoteGetNotes(searchWords=""):
    filter = NoteStore.NoteFilter(order = Types.NoteSortOrder.UPDATED)
    filter.words = searchWords

    meta = NoteStore.NotesMetadataResultSpec()
    meta.includeTitle        = True
    meta.includeNotebookGuid = True
    meta.includeTagGuids     = True

    count  = Limits.EDAM_USER_NOTES_MAX
    result = noteStore.findNotesMetadata(authToken, filter, 0, count, meta)
    update_count = lambda c: max(c - len(result.notes), 0)
    count = update_count(count)

    while ((result.totalNotes != len(result.notes)) and count != 0):
        offset = len(result.notes)
        result.notes += noteStore.findNotesMetadata(
            authToken, filter, offset, count, meta).notes
        count = update_count(count)

    notes = []
    for key, note in enumerate(result.notes):
        notes.append(note)

    return notes

#
def EvernoteGetNotebook(guid):
    try:
        return noteStore.getNotebook(authToken, guid)
    except:
        return None

#
def EvernoteGetNotebooks():
    return noteStore.listNotebooks(authToken)

#
def EvernoteGetTags():
    return noteStore.listTags(authToken)

#
def EvernoteLoadNote(note):
    return noteStore.getNote(authToken, note.guid, True, False, False, False)

#
def EvernoteRefreshNoteMeta(note):
    return noteStore.getNote(authToken, note.guid, False, False, False, False)

#
def EvernoteUpdateNote(note):
    noteStore.updateNote(authToken, note)

#
def EvernoteUpdateNotebook(notebook):
    noteStore.updateNotebook(authToken, notebook)

