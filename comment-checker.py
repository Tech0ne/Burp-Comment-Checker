from burp import IBurpExtender, IContextMenuFactory
from java.io import PrintWriter

from java.util import ArrayList
from javax.swing import JMenuItem

def retreive_comments_from_html(code):
    """:param code: HTML code to scan for comments"""
    if not "<!--" in code:
        return []
    comments = []
    for e in code.split("<!--")[1:]:
        comments.append(e.split("-->")[0])
    return comments

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = self.callbacks.getHelpers()
        self.context = None

        self.callbacks.setExtensionName("Comment scanner")
        self.callbacks.registerContextMenuFactory(self)
    
    def createMenuItems(self, context_menu):
        self.context = context_menu

        menu_list = ArrayList()
        menu_list.add(JMenuItem("Scan for comments", actionPerformed=self.scanForComment))
        return menu_list
    
    def scanForComment(self, event):
        http_trafic = self.context.getSelectedMessages()
        for trafic in http_trafic:
            for comment in retreive_comments_from_html(trafic.response.tostring()):
                print("Got a comment : %s" % comment)