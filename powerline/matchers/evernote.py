# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

import os
import re

from powerline.bindings.vim import buffer_name

EVERNOTE_RE = re.compile('__Evernote__')

def evernote(matcher_info):
	name = buffer_name(matcher_info)
	return name and EVERNOTE_RE.match(os.path.basename(name))

EVERNOTE_EXPLORER_RE = re.compile('__EvernoteExplorer__')

def evernote_explorer(matcher_info):
	name = buffer_name(matcher_info)
	return name and EVERNOTE_EXPLORER_RE.match(os.path.basename(name))
