import html2text
import vim_evernote_markdown2
from base64 import b64encode, b64decode

from config import *

VIM_EVERNOTE_COMMENT_BEG = '<!-- vim:'
VIM_EVERNOTE_COMMENT_END = '-->'

#
# Convert enmal to text use html2text
#
def ENMLtoText(contentENML):
    html2text.EMPHASIS_MARK = '*'
    html2text.UL_ITEM_MARK = '*'
    html2text.STRONG_MARK = '**'

    builtin = contentENML.find(VIM_EVERNOTE_COMMENT_BEG, 0, 150)
    if builtin >= 0:
        try:
            builtin_end = contentENML.find(VIM_EVERNOTE_COMMENT_END, builtin)
            bmdtxt = contentENML[builtin+len(VIM_EVERNOTE_COMMENT_BEG):builtin_end]
            content = b64decode(bmdtxt.encode('utf8')).decode('utf8')
        except:
            content = ''

    if builtin < 0 or content == '':
        try:
            content = html2text.html2text(contentENML)
        except:
            content = contentENML

    return content

#
# Convert text to enml use python-markdown2
#
def textToENML(content):
    body = markdown2.markdown(content, extras = MD_EXTRAS)

    if 'inline-css' in MD_EXTRAS:
        if 'body' in MD_EXTRAS['inline-css']:
            wrapper_style = MD_EXTRAS['inline-css']['body']

    contentENML = '<?xml version="1.0" encoding="UTF-8"?>'
    contentENML += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
    contentENML += '<en-note style="%s">' % wrapper_style
    hidden = ('\n%s%s%s\n' %
                (VIM_EVERNOTE_COMMENT_BEG,
                 b64encode(content.encode('utf8')).decode('utf8'),
                 VIM_EVERNOTE_COMMENT_END))
    contentENML += hidden
    contentENML += body
    contentENML += '</en-note>'

    return contentENML
