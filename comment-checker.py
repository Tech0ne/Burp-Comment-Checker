from burp import IBurpExtender, ITab, IContextMenuFactory
from java.awt import BorderLayout
from java.util import ArrayList
from javax.swing import JPanel, JTable, JScrollPane, JMenuItem
from javax.swing.table import AbstractTableModel

INSTRESTING_WORDS = ["pass", "password", "user", "username", "name", "cmd", "command", "vuln", "xploit", "help"]

def retreiveCommentsFromHTML(code):
    if not "<!--" in code:
        return []
    comments = []
    for e in code.split("<!--")[1:]:
        comments.append(e.split("-->")[0])
    return comments

def handleCustomChar(char):
    specialChars = {
        0: '0',
        7: 'a',
        8: 'b',
        9: 't',
        10: 'n',
        11: 'v',
        12: 'f',
        13: 'r'
    }
    if not ord(char) in specialChars.keys():
        return 'x' + str(int(ord(char), base=16))
    return specialChars[ord(char)]

def beautifyString(string):
    final = ""
    for char in string:
        if ord(char) <= 31 or ord(char) >= 127:
            final += " \\" + handleCustomChar(char) + ' '
        else:
            final += char
    return final

def isImportant(comment):
    for passcode in INSTRESTING_WORDS:
        if passcode in comment:
            return "/!\\ Comment contains \"%s\" /!\\  " % (passcode)
    return ""

class BurpExtender(IBurpExtender, ITab, AbstractTableModel, IContextMenuFactory):
    def	registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Comments Viewer")

        self._comments = ArrayList()
        self.context = None

        self.mainPanel = JPanel(BorderLayout())
        commentsTable = Table(self)
        commentsScrollPane = JScrollPane(commentsTable)
        self.mainPanel.add(commentsScrollPane)

        callbacks.addSuiteTab(self)
        callbacks.registerContextMenuFactory(self)
        
        return

    def createMenuItems(self, invocation):
        self.context = invocation
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Fetch comments", actionPerformed=self.searchURLs))
        return menu_list

    def searchURLs(self, _):
        if not self.context:
            return
        httpTrafic = self.context.getSelectedMessages().tolist()
        for req in httpTrafic:
            code = req.getResponse().tostring()
            for comment in retreiveCommentsFromHTML(code):
                formated = "%sComment found on page   \"%s\" :       \"%s\"%s" % (isImportant(comment), req.getUrl().toString(), beautifyString(comment))
                row = self._comments.size()
                self._comments.add(formated)
                self.fireTableRowsInserted(row, row)
        
    def getTabCaption(self):
        return "Comment-Scanner"
    
    def getUiComponent(self):
        return self.mainPanel
    
    def getRowCount(self):
        try:
            return self._comments.size()
        except:
            return 0

    def getColumnCount(self):
        return 1

    def getColumnName(self, _):
        return "Fetched comments"

    def getValueAt(self, rowIndex, _):
        logEntry = self._comments.get(rowIndex)
        return logEntry
    
class Table(JTable):
    def __init__(self, extender):
        self._extender = extender
        self.setModel(extender)
    
    def changeSelection(self, row, col, toggle, extend):
        logEntry = self._extender._comments.get(row)
        self._extender._currentlyDisplayedItem = logEntry
        JTable.changeSelection(self, row, col, toggle, extend)