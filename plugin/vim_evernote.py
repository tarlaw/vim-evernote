import vim
import re

from explorer import Explorer
from view     import *
from utils    import *
from enml     import *

import evernote.edam.type.ttypes  as Types
import evernote.edam.error.ttypes as Errors

#
# +----------+---------------------------+
# |          |                           |
# |          |                           |
# | explorer |           view            |
# |          |                           |
# |          |                           |
# +----------+---------------------------+
#
# vim_geeknote.vim --> vim_geeknote.py --> explorer.py
#                                |            |
#                                |            |
#                                |            V
#                                +-------> view.py
#

#======================== Globals ============================================#

explorer = Explorer()

#======================== Evernote Functions  ================================#

def EvernoteActivateNode():
    explorer.activateNode(vim.current.line)

def EvernoteCommitStart():
    explorer.commitChanges()

def EvernoteCommitComplete():
    explorer.render()

def EvernoteCreateNote(title):
    #
    # Figure out what notebook to place the note in. Give preference to the
    # notebook selected in the explorer window (if one is selected). Otherwise,
    # place it into the default notebook.
    #
    notebook = explorer.getSelectedNotebook()
    if notebook is None:
        notebook = EvernoteGetDefaultNotebook()

    if notebook is None:
        vim.command('echoerr "Please select a notebook first."')
        return

    # Cleanup the title of the note.
    title = title.strip('"\'')

    # Finally, create and open a blank note.
    note              = Types.Note()
    note.title        = title
    note.guid         = None
    note.created      = None
    note.notebookGuid = notebook.guid

    note = EvernoteCreateNewNote(note)
    EvernoteOpenNote(note)

    # Add the note to the navigation window.
    explorer.addNote(note)

def EvernoteCreateNotebook(name):
    notebook = Types.Notebook()
    notebook.name = name.strip('"\'')
    try:
        notebook = EvernoteCreateNewNotebook(notebook)
    except:
        vim.command('echoerr "Failed to create notebook."')

    explorer.addNotebook(notebook)

def EvernoteHandleNoteSaveFailure(note, e):
    print e
    msg  = '+------------------- WARNING -------------------+\n'
    msg += '|                                               |\n'
    msg += '| Failed to save note (see error above)         |\n'
    msg += '|                                               |\n'
    msg += '| Save buffer to a file to avoid losing content |\n'
    msg += '|                                               |\n'
    msg += '+------------------- WARNING -------------------+\n'
    vim.command('echoerr "%s"' % msg)

def EvernoteSaveAsNote():
    global explorer

    #
    # Figure out what notebook to place the note in. Give preference
    # to the notebook selected in the explorer window (if one is
    # selected). Otherwise, place it into the default notebook.
    #
    notebook = None
    if explorer is not None:
        notebook = explorer.getSelectedNotebook()

    if notebook is None:
        notebook = EvernoteGetDefaultNotebook()

    if notebook is None:
        vim.command('echoerr "Please select a notebook first."')
        return

    title = ''
    rows  = len(vim.current.buffer)
    if rows > 0:
        title = vim.current.buffer[0].strip()
    else:
        vim.command('echoerr "Cannot save empty note."')
        return

    content = ''
    if rows > 1:
        start = 1
        while start < rows:
            if vim.current.buffer[start].strip() != '':
                break
            start += 1
        for r in range(start, len(vim.current.buffer)):
            content += vim.current.buffer[r] + '\n'

        note         = Types.Note()
        note.title   = title
        note.content = textToENML(content)
        note.created = None
        note.notebookGuid = notebook.guid

    try:
        note = EvernoteCreateNewNote(note)
        note = EvernoteLoadNote(note)
    except Exception as e:
        EvernoteHandleNoteSaveFailure(note, e)
        return

    EvernoteOpenNote(note)

    # Add the note to the navigation window.
    explorer.addNote(note)

def EvernoteSaveNote(filename):
    note    = EvernoteGetOpenNote(filename)
    changed = EvernoteCommitChangesToNote(note)
    if changed:
        try:
            EvernoteUpdateNote(note)
        except Exception as e:
            EvernoteHandleNoteSaveFailure(note, e)

def EvernoteSearch(args):
    notes = EvernoteGetNotes(args)

    explorer.clearSearchResults()
    explorer.addSearchResults(notes)
    explorer.render()

def EvernoteSync():
    explorer.commitChanges()
    explorer.refresh()
    explorer.render()

def EvernoteTerminate():
    EvernoteCloseAllNotes()

def EvernoteToggle():
    global explorer

    if explorer.isHidden():
        explorer.show()
    else:
        explorer.hide()

