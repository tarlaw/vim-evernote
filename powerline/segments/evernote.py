# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

try:
	import vim
except ImportError:
	vim = object()

from powerline.bindings.vim import bufvar_exists
from powerline.segments.vim import window_cached


@window_cached
def evernote_get_note_title(pl):
	if not bufvar_exists(None, 'EvernoteTitle'):
		return None

	title = vim.eval('getbufvar("%", "EvernoteTitle")')
	return [{
		'contents': title,
		'highlight_group': ['file_name'],
	}]

def evernote_get_notebook_name(pl):
	if not bufvar_exists(None, 'EvernoteNotebook'):
		return None

	name = vim.eval('getbufvar("%", "EvernoteNotebook")')
	return [{
		'contents': name,
		'highlight_group': ['file_name'],
	}]
