# -*- coding: utf-8 -*-

'''This module contains the AdiumChatOutput class'''
import base64

from PyQt4      import QtGui
from PyQt4      import QtCore
from PyQt4      import QtWebKit

import e3
import gui
from gui.base import Plus
from gui.qt4ui  import Utils
from gui.qt4ui.Utils import tr


class AdiumChatOutput (QtGui.QScrollArea):
    '''A widget which displays various messages of a conversation 
    using Adium themes'''
    # pylint: disable=W0612
    NAME = 'AdiumChatOutput'
    DESCRIPTION = 'A widget to display conversation messages with Adium' \
                  'themes. Based on Webkit technology.'
    AUTHOR = 'Gabriele "Whisky" Visconti'
    WEBSITE = ''
    # pylint: enable=W0612
    
    
    def __init__(self, config, parent=None):
        QtGui.QScrollArea.__init__(self, parent)
        
        self.theme = gui.theme.conv_theme
        self.config = config
        self._qwebview = QtWebKit.QWebView(self)
        
        self.setWidget(self._qwebview)
        self.setWidgetResizable(True)
        self._qwebview.setRenderHints(QtGui.QPainter.SmoothPixmapTransform)
        self._qwebview.page().setLinkDelegationPolicy(
                                    QtWebKit.QWebPage.DelegateAllLinks)
        
        pic = gui.theme.image_theme.user
        body = gui.theme.conv_theme.get_body('', '', '', pic, pic)
        self._qwebview.setHtml(body)
        
        self._qwebview.linkClicked.connect(
                        lambda qt_url: gui.base.Desktop.open(qt_url.toString()) )

    def clear(self, source="", target="", target_display="",
            source_img="", target_img=""):
        '''clear the content'''
        body = self.theme.get_body(source, target, target_display, source_img,
                target_img)
        self._qwebview.setHtml(body)

    def _append_message(self, msg, scroll=True):
        '''add a message to the conversation'''

        html = self.theme.format(msg, scroll)

        self._qwebview.page().mainFrame().evaluateJavaScript(html)

    def send_message(self, formatter, msg):
        '''add a message to the widget'''
        self._append_message(msg, self.config.b_allow_auto_scroll)

    def receive_message(self, formatter, msg):
        '''add a message to the widget'''
        self._append_message(msg, self.config.b_allow_auto_scroll)

    def information(self, formatter, msg):
        '''add an information message to the widget'''
        msg.message = Plus.msnplus_strip(msg.message)
        self._append_message(msg, self.config.b_allow_auto_scroll)

    def update_p2p(self, account, _type, *what):
        ''' new p2p data has been received (custom emoticons) '''
        if _type == 'emoticon':
            _creator, _friendly, path = what
            _friendly = xml.sax.saxutils.unescape(_friendly)
            #see gui/base/MarkupParser.py:
            _id = base64.b64encode(_creator + _friendly) 
            mystr = '''
                        var now=new Date();
                        var x=document.images;
                        for (var i=0; i<x.length; i++){
                            if (x[i].name=='%s') {
                                x[i].src='%s?'+now.getTime();
                            }
                       }''' % (_id, path)
            self._qwebview.page().mainFrame().evaluateJavaScript(mystr)

