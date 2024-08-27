import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Multiple Windows Example')

        # Crear panel principal
        self.panel = wx.Panel(self)

        # Crear barra de herramientas
        self.InitUI()

        # Crear sizer vertical para contener las ventanas
        self.window_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Crear sizer principal
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.window_sizer, 1, wx.EXPAND | wx.ALL, border=20)

        self.panel.SetSizer(self.main_sizer)

    def InitUI(self):
        self.menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        viewMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        viewItem = viewMenu.Append(wx.ID_VIEW_LIST, 'View', 'Add window')
        self.menubar.Append(fileMenu, '&File')
        self.menubar.Append(viewMenu, '&View')
        self.SetMenuBar(self.menubar)  # Establecer el wx.MenuBar directamente en la ventana

        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)
        self.Bind(wx.EVT_MENU, self.on_new_window, viewItem)

        self.SetSize((500, 300))
        self.SetTitle('Simple menu')
        self.Centre()

        self.child_windows = []

    def OnQuit(self, e):
        self.Close()

    def on_new_window(self, event):
        # Crear nueva ventana
        new_window = ChildFrame(self.panel)  # Cambiar el padre a self.panel
        
        self.child_windows.append(new_window)
        self.window_sizer.Add(new_window, 1, wx.EXPAND)
        self.main_sizer.Layout()
        new_window.Show()

class ChildFrame(wx.Panel):  # Cambiar a Panel para que se ajuste mejor
    def __init__(self, parent):
        super().__init__(parent)

        # Crear sizer para el contenido de la ventana
        self.content_sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetWindowStyle(wx.BORDER_RAISED)

        # Agregar contenido a la ventana
        text = wx.StaticText(self, label='This is a child window.')
        self.content_sizer.Add(text, 0, wx.ALL | wx.EXPAND, 10)  # Bordes alrededor del texto

        # Agregar un botón para cerrar este panel
        close_button = wx.Button(self, label='Close Panel')
        self.content_sizer.Add(close_button, 0, wx.ALL | wx.CENTER, 10)  # Bordes alrededor del botón

        # Establecer el sizer en el panel
        self.SetSizer(self.content_sizer)

        # Opcional: Establecer un borde alrededor del panel
        self.SetBackgroundColour(wx.Colour(240, 240, 240))  # Cambiar el color de fondo del panel
        self.SetMinSize((300, 200))

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()