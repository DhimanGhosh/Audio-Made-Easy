import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(1600, 800))

        self.panel = MyPanel(self)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
        
        self.label = wx.StaticText(self, label='Hello There', style=wx.ALIGN_CENTER)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        vbox.Add(self.label, 0, wx.EXPAND)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="First Window")
        self.frame.Show()

        return True

app = MyApp()
app.MainLoop()
