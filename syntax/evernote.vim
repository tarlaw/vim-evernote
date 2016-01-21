syn match EvernoteSep         #=\+#

syn match EvernoteNotebookKey #N\[.\+\]#
syn match EvernoteNoteKey     #n\[.\+\]#
syn match EvernoteTagKey      #T\[.\+\]#

syn match EvernoteNotebook    #^.\+N\[.\+\]# contains=EvernoteNotebookKey
syn match EvernoteNote        #^.\+n\[.\+\]# contains=EvernoteNoteKey
syn match EvernoteTag         #^.\+T\[.\+\]# contains=EvernoteTagKey

hi def link EvernoteNotebookKey ignore
hi def link EvernoteNoteKey     ignore
hi def link EvernoteTagKey      ignore
hi def link EvernoteSep         Question
hi def link EvernoteNotebook    Title
hi def link EvernoteTag         Title
hi def link EvernoteNote        Type
