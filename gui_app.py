import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(1600, 800))

        self.panel = MyPanel(self)

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)
        
        self.label1 = wx.StaticText(self, label='This is Label 1', style=wx.ALIGN_CENTER)
        self.label2 = wx.StaticText(self, label='This is Label 2', style=wx.ALIGN_CENTER)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        vbox.Add(self.label1, 0, wx.EXPAND)
        hbox.Add(self.label2, 0, wx.EXPAND)

        self.SetSizer(vbox)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="First Window")
        self.frame.Show()

        return True

app = MyApp()
app.MainLoop()
