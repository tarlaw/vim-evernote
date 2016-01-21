# vim-evernote

[Evernote](http://www.evernote.com) Plugin for Vim. This plugin forked from
[vim-geeknote](https://github.com/neilagabriel/vim-geeknote) with geeknote
needed removed and reuse enmal to text part of
[sublime-evernote](https://github.com/bordaigorl/sublime-evernote).

## Intro 

Integrates Evernote/Evernote into Vim and Neovim.
- Notebook navigation, creation, and renaming
- Note viewing, renaming, editing, and creation.

## Screenshots

![img](https://github.com/neilagabriel/vim-geeknote/blob/master/img/explorer.png)

## Dependencies/Requirements

- Vim 7.4.364 or newer (issues observed with earlier versions)
- Linux or OSX (not tested on Windows)

## Installation

1. Use your plugin manager of choice to install plugin.

* [Vundle](https://github.com/gmarik/vundle)
   * Add `Bundle 'https://github.com/tarlaw/vim-evernote'` to .vimrc
   * Run `:BundleInstall`
* [Pathogen](https://github.com/tpope/vim-pathogen)
   * `git clone https://github.com/tarlaw/vim-evernote ~/.vim/bundle/`

2. If using macvim, refer to [README_mac.md](README_mac.md) for additional instructions.

3. Modify `~/.vim/bundle/vim-evernote/plugin/config_example.py` add `authToken`
   and `noteStoreUrl`. Modify `config_example.py` to `config.py`. I think this
   config method is not good, but I don't know how to.

## Optional Setup and Configuration

### Quick toggle

    noremap <F8> :Evernote<cr>

### Navigation Window Behavior

#### Limit Width

By default, vim-evernote will attempt to resize the navigation window based on
its current content, up to 40 columns. If you have notebooks or notes with very
long names you may want to use the following option:

    let g:EvernoteMaxExplorerWidth=<value>

Where `<value>` is replaced with the max width of the window. Depending on the
value you specify, this could be used to increase the cap in order to view
longer names or decrease it to keep the navigation window even smaller.

#### Fix Width

Use the following option to fix the width of the window to a specific value:

    let g:EvernoteExplorerWidth=<value>

Where `<value>` is replaced with the desired width of the window. This option
overrides all other width-related options.

#### Limit View to Specific Notebooks

##### By GUID

By default, all notebooks will be shown in the navigation window. Depending on
the number notebooks you have, this can add a non-trivial amount of time to the
load time of the plugin. You may also simply not want to see your full set of
notebooks when working in Vim. Use the following option to limit the display to
a specific notebook or set of notebooks:

    let g:EvernoteNotebooks=
    \    [
    \        'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee', 
    \        'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee', 
    \    ]

##### By Expression

Notebooks can also be filtered by expressions. Use the following option to
specify a list of regular expressions to apply to each notebook to decide if it
should be included in the navigation window. Unlike filtering by GUID, this
option does *not* yield a performance improvement. In fact, it may slightly
degrade it depending on the number of expressions you specify.

    let g:EvernoteNotebookFilters=
    \    [
    \        'Unsorted'          ,
    \        '^Status - WW(\d+)$',
    \    ]

### Explorer Special Characters

The following options may be used to customize the characters used to denote
opened/closed notebooks and tags:

    let g:EvernoteExplorerNodeClosed = '+'
    let g:EvernoteExplorerNodeOpened = '-'

Both unicode and ascii characters are supported.

### Launching

It may sometimes be convenient to launch geeknote in a new instance of Vim. An
alias can be helpful for this. Here an example for `bash`:

    alias vim-evernote='vi -c Evernote'

### Powerline

Powerline may be used to improve the look of the navigation window as well as
any notes that you open. At this time however, if you'd like this support,
you'll need to use my personal powerline fork locate here:

    https://github.com/neilagabriel/powerline.git

Just install it in the normal fashion and everything should just work.

### Evernote Autocommands

vim-evernote uses FileType `evernote` for the navigation window. This may be
used to set your own custom behavior. For example, the following disables line
numbers in the navigation window:

    autocmd FileType evernote setlocal nonumber

### Filesystem

vim-evernote uses temporary files to display the navigation window and for any
notes that are opened. By default, files are created in the system temp
directory (ie. `TMPDIR`, `TEMP`, or `TMP`). The following option allows the
user to specify where all temp (or scratch) files should be maintained. Note
that vim-evernote will attempt to cleanup after itself when it is proper to do
so.

    let g:EvernoteScratchDirectory=<path>

Where `<path>` is replaced with the desired filesystem location for any and all
temp files created by vim-evernote. *Note that the path must exist.* The plugin
will not attempt to create it.

## Usage

### Toggle Evernote Navigation Window

Use `:Evernote` to open/toggle the geeknote navigation window. If the
navigation window is not visible, this command will split the current window
vertically and display the navigation window on the left-side. If visible, the
navigation window will be hidden. Notebooks can be expanded to show the notes
they contain.  To expand a notebook, simply navigate to the name of the
notebook and hit `<Enter>`. Hit `<Enter>` again to close the notebook. To
open/view a note, navigate to the note and hit `<Enter>`. The note will be
displayed in the previous window if it is possible to do so or in a new
vertical split. To save changes to the note, simply save the buffer (e.g.
`:w`). The title of the note will be shown on the first line. The title line
should not be deleted from the buffer but *may* be modified to rename the note.

### Creating Notebooks

Use `:EvernoteCreateNotebook <name>` to create a new notebook.

### Creating Notes

Use `:EvernoteCreateNote <name>` to create a new note. The note will be created
in the notebook currently selected in the navigation window. If a notebook is
not selected, the note will be created in the default notebook. A new buffer
for the note will be displayed in the previous window if it is possible to do
so or in a new vertical split.

Use `:EvernoteSaveAsNote` to create a new note using the content of the current
buffer. The first line in the buffer will be used as the note's title. The
remainder of the buffer will be saved as note content. Note this this command
will create and switch to a new buffer.

### Renaming Notebooks and Notes

To rename notebooks or notes, simply modify the name of the notebook/note in
the navigation window and save the bugger (e.g. `:w`). Any number of changes
can be made before saving, but be sure not to modify an item's GUID.

### Moving Notes

To move a note into a different notebook, simply move the note's text (includes
title and GUID) under the desired notebook in the navigation window and save
the buffer. Similar to renaming, any number notes can be moved before saving
the buffer.

### Synchronization 

Use `:EvernoteSync` to update the navigation with the latest data on the
Evernote server. Warning, any notes that are opened when this command is issued
will not be updated. Support for this will be added in future releases.

### Searching

Use `:EvernoteSearch <text>` to search for notes with specific `text` in their
titles' and/or content. All results will be added to the nagivation window.

## Acknowledgments

- [vim-geeknote](https://github.com/neilagabriel/vim-geeknote)
- [sublime-evernote](https://github.com/bordaigorl/sublime-evernote)

