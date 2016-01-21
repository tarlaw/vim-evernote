#!/usr/bin/env python
import vim
import os

from enml  import *
from utils import *
from conn  import *

# Maps buffer names to NoteTracker objects.
openNotes = {}

#
# Holds all information that needs to be tracked for any note that has been
# opened.
#
class NoteTracker(object):
    def __init__(self, note, buffer):
        self.note     = note
        self.buffer   = buffer
        self.modified = False

# Close all opened notes.
def EvernoteCloseAllNotes():
    #
    # Try to delete any temp files that still exist (is is possible that
    # some/all were already garbage collected by the OS.
    #
    try:
        for filename in openNotes:
            os.remove(filename)
    except:
        pass

    openNotes.clear()

# Close the note associated with the given buffer name.
def EvernoteCloseNote(filename):
    if filename in openNotes:
        os.remove(filename)
        del openNotes[filename]

# Commit any changes that were made to the note in the buffer to the note.
def EvernoteCommitChangesToNote(note):
    tracker = EvernoteGetNoteTracker(note)

    # If the note has not been modified, there's nothing more to do.
    if tracker.modified is False:
        return False

    #
    # Now that we know the note has been modified, read the note's buffer and
    # pull out the note's title and content.
    #
    content = ''
    title   = tracker.note.title
    lines   = open(tracker.buffer.name, 'r').readlines()
    if len(lines) > 0:
        title = lines.pop(0).strip()
        while len(lines) > 0:
            if lines[0].strip() == '':
                lines.pop(0)
            else:
                break
    for r in lines:
        content += r

    # Update the note's title and content from what was read from the buffer.
    tracker.note.title   = title
    tracker.note.content = textToENML(content)

    return True

# Find the object that is tracking the given note (None if note opened).
def EvernoteGetNoteTracker(note):
    for filename in openNotes:
        if openNotes[filename].note.guid == note.guid:
            return openNotes[filename]
    return None

# Given the name of a buffer, find the note that the buffer represents.
def EvernoteGetOpenNote(filename):
    if filename in openNotes:
        return openNotes[filename].note
    return None

# Determine if the note has been modified since since it was last saved.
def EvernoteNoteIsModified(note):
    tracker = EvernoteGetNoteTracker(note)
    return tracker.modified

# Determine if the user has already opened the given note.
def EvernoteNoteIsOpened(note):
    tracker = EvernoteGetNoteTracker(note)
    return True if tracker is not None else False

# Open a note in the active window.
def EvernoteOpenNote(note):
    #
    # Determine which window to display the note in (creating one if necessary)
    # and switch to that window.
    #
    origWin = getActiveWindow()
    prevWin = getPreviousWindow()

    setActiveWindow(prevWin)
    isPrevUsable = EvernoteIsWindowUsable(prevWin)
    if isPrevUsable is False:
        firstUsableWin = EvernoteGetFirstUsableWindow()
        if firstUsableWin != -1:
            setActiveWindow(firstUsableWin)
        else:
            vim.command('vertical new')

    #
    # Check to see if the note is already opened before opening it in a new
    # buffer.
    #
    opened = EvernoteNoteIsOpened(note)
    if opened is False:
        # Load the note's content
        note    = EvernoteLoadNote(note)
        content = ENMLtoText(note.content)
        #content = tools.stdoutEncode(content)

        # Write the note's title and content to a temporary file.
        f = createTempFile(delete=False)
        f.write(note.title + '\n\n')

        isNoteEmpty = not content.strip()
        if isNoteEmpty is False:
            f.write(content)
        else:
            f.write("<add content here>\n")
        f.flush()

        # Now edit the file in a new buffer within the active window.
        vim.command('edit {}'.format(f.name))

        # Close the file now that it is open in the buffer.
        f.close()

        # Position the cursor at a convenient location if opening an empty note
        if isNoteEmpty:
            vim.current.window.cursor = (3, 0)

        #
        # Create an object to keep track of the note and all associated
        # information while it's opened.
        #
        openNotes[f.name] = NoteTracker(note, vim.current.buffer)

        # Register callbacks for the buffer events that affect the note.
        autocmd('BufWritePre',
                '<buffer>',
                ':call Vim_EvernotePrepareToSaveNote("{}")'.format(f.name))

        autocmd('BufWritePost',
                '<buffer>',
                ':call Vim_EvernoteSaveNote("{}")'.format(f.name))

        autocmd('BufDelete',
                '<buffer>',
                ':call Vim_EvernoteCloseNote("{}")'.format(f.name))

        vim.command("let b:EvernoteTitle=\"%s\"" % note.title)
        notebook = EvernoteGetNotebook(note.notebookGuid)
        vim.command("let b:EvernoteNotebook=\"%s\"" % notebook.name)
    #
    # Otherwise, the note has aleady been opened. Simply switch the active window
    # to the note's buffer.
    #
    else:
        tracker = EvernoteGetNoteTracker(note)
        vim.command("buffer {}".format(tracker.buffer.name))

    #
    # By default, Evernote expects to receive notes with markdown-formated
    # content. Set the buffer's 'filetype' and 'syntax' options.
    #
    # TODO: Figure out why setting the 'syntax' buffer option alone does not
    #       enable syntax highlighting and why setlocal is needed instead.
    #
    # vim.current.buffer.options['filetype'] = 'markdown'
    # vim.command('setlocal syntax=markdown')

    # Now restore the original window.
    setActiveWindow(origWin)

def EvernotePrepareToSaveNote(filename):
    filename = os.path.abspath(filename)
    tracker  = openNotes[filename]
    tracker.modified = tracker.buffer.options['modified']

def EvernoteGetFirstUsableWindow():
   wnum = 1
   while wnum <= winnr('$'):
       bnum         = winbufnr(wnum)
       buftype      = getBufferVariable(bnum, 'buftype')
       isModified   = getBufferVariable(bnum, 'modified')
       isPreviewWin = getWindowVariable(wnum, 'previewwindow')
       name         = getBufferName(bnum)

       if ((bnum != -1)                 and
           (buftype == '')              and
           (name == '')                 and
           (isPreviewWin is False)      and
           ((isModified  is False)      or
               hidden())):
           return wnum
       wnum += 1
   return -1


def EvernoteIsWindowUsable(wnum):
    if winnr('$') == 1:
        return False

    bnum    = vim.windows[wnum-1].buffer.number
    buftype = getBufferVariable(bnum, 'buftype')
    preview = getWindowVariable(wnum, 'previewwindow')

    #
    # If the window's buffer has a special type or is the preview window, it is
    # not usable.
    #
    if (buftype != '') or (preview is True):
        return False

    # If the user has the 'hidden' option set, the window is usable.
    if hidden():
        return True

    #
    # If the window's buffer belongs to an unmodified note, the window is
    # usable.
    #
    name = getBufferName(bnum)
    if name in openNotes:
        isModified = getBufferVariable(bnum, 'modified')
        if isModified is False:
            return True

    # If the buffer is open in more than one window, the window is usable.
    return bufInWindows(winbufnr(wnum)) > 1

