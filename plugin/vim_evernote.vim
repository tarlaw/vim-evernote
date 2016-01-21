python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))

" ---------------------- Configuration ----------------------------------------

if has('nvim')
    let g:EvernoteNeovimMode="True"
endif

" ---------------------- Functions --------------------------------------------

function! Vim_EvernoteTerminate()
python << endOfPython
from vim_evernote import EvernoteTerminate
EvernoteTerminate()
endOfPython
endfunction

function! Vim_EvernoteToggle()
python << endOfPython
from vim_evernote import EvernoteToggle
EvernoteToggle()
endOfPython
endfunction

function! Vim_EvernoteActivateNode()
python << endOfPython
from vim_evernote import EvernoteActivateNode
EvernoteActivateNode()
endOfPython
endfunction

function! Vim_EvernoteCloseNote(arg1)
python << endOfPython
from vim_evernote import EvernoteCloseNote
filename = vim.eval("a:arg1")
EvernoteCloseNote(filename)
endOfPython
endfunction

function! Vim_EvernoteCreateNotebook(arg1)
python << endOfPython
from vim_evernote import EvernoteCreateNotebook
name = vim.eval("a:arg1")
EvernoteCreateNotebook(name)
endOfPython
endfunction

function! Vim_EvernoteCreateNote(arg1)
python << endOfPython
from vim_evernote import EvernoteCreateNote
name = vim.eval("a:arg1")
EvernoteCreateNote(name)
endOfPython
endfunction

function! Vim_EvernoteSaveAsNote()
python << endOfPython
from vim_evernote import EvernoteSaveAsNote
EvernoteSaveAsNote()
endOfPython
endfunction

function! Vim_EvernoteSearch(arg1)
python << endOfPython
from vim_evernote import EvernoteSearch
args = vim.eval("a:arg1")
EvernoteSearch(args)
endOfPython
endfunction

function! Vim_EvernotePrepareToSaveNote(arg1)
python << endOfPython
from vim_evernote import EvernotePrepareToSaveNote
filename = vim.eval("a:arg1")
EvernotePrepareToSaveNote(filename)
endOfPython
endfunction

function! Vim_EvernoteSaveNote(arg1)
python << endOfPython
from vim_evernote import EvernoteSaveNote
filename = vim.eval("a:arg1")
EvernoteSaveNote(filename)
endOfPython
endfunction

function! Vim_EvernoteSync()
python << endOfPython
from vim_evernote import EvernoteSync
EvernoteSync()
endOfPython
endfunction

function! Vim_EvernoteCommitStart()
python << endOfPython
from vim_evernote import EvernoteCommitStart
EvernoteCommitStart()
endOfPython
endfunction

function! Vim_EvernoteCommitComplete()
python << endOfPython
from vim_evernote import EvernoteCommitComplete
EvernoteCommitComplete()
endOfPython
endfunction

" ---------------------- User Commands ----------------------------------------

command!          Evernote               call Vim_EvernoteToggle()
command! -nargs=1 EvernoteCreateNotebook call Vim_EvernoteCreateNotebook(<f-args>)
command! -nargs=1 EvernoteCreateNote     call Vim_EvernoteCreateNote(<f-args>)
command!          EvernoteSaveAsNote     call Vim_EvernoteSaveAsNote()
command! -nargs=* EvernoteSearch         call Vim_EvernoteSearch(<q-args>)
command!          EvernoteSync           call Vim_EvernoteSync()
