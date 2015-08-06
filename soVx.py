import VxSim
import os
import wx

class WindowPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        '''Panel containing all main contents of soVx window'''
        wx.Panel.__init__(self, parent, *args, **kwargs)

        Vx = WindowVx(self)
        self.parent = parent
        self.current_directory = os.getcwd()

        b_browse_config = wx.Button(self, label='config')
        b_browse_config.Bind(wx.EVT_BUTTON, self.browse_file)

        b_start = wx.Button(self, label='Run')
        b_start.Bind(wx.EVT_BUTTON, Vx.vx_loader)

        b_run = wx.Button(self, label='Step')
        b_run.Bind(wx.EVT_BUTTON, Vx.vx_step)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # Position all objects within the panel
        sizer.Add(b_browse_config, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add(b_start, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add(b_run, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.SetSizerAndFit(sizer)

    def browse_file(self, event):
        '''Opens a file browser in cwd.'''
        dlg = wx.FileDialog(
                self, message = 'Choose a file to load',
                defaultDir = self.current_directory,
                defaultFile = '',
                style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print ('File selected:')
            for path in paths:
                print path
        dlg.Destroy()

class WindowVx(WindowPanel):

    def __init__(self, *args, **kwargs):
        '''Create VxSim constants for contained functions.'''
        self.app = VxSim.VxApplication()
        self.config = ''
        self.scene = ''
        self.gtm_mechanism = ''
        self.scenario_json = ''
        self.mechanism = ''

    def vx_loader(self, event=None):
        '''Loads the scene into SimApp with selected files'''

        serializer = VxSim.VxApplicationConfigSerializer()
        serializer.load('A:/builds/PTLEN/assets/STAGE/resources/config/qa.vxc')

        if serializer.isValid():
            config = serializer.getApplicationConfig()
            config.apply(self.app)

        scene = self.app.getSimulationFileManager().loadScene('A:/builds/PTLEN/assets/STAGE/assets/Scenario/STS/PTLen_STS.vxs', 'ContentExtensionScene')
        self.app.add(scene)

        return self.config
        return self.scene

    def vx_step(self, event=None):
        '''Steps the scene the selected number of times. 
        The soVx window will become unresponsive during this time.'''
        for i in range(0,500):
            self.app.update()

class WindowFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        '''Main frame holding "WindowPanel".'''
        wx.Frame.__init__(self, *args, **kwargs)

        MenuBar = wx.MenuBar()
        FileMenu = wx.Menu()

        item = FileMenu.Append(wx.ID_EXIT, text="&Quit")
        self.Bind(wx.EVT_MENU, self.menu_quit, item)

        MenuBar.Append(FileMenu, "&File")
        self.SetMenuBar(MenuBar)

        self.Panel = WindowPanel(self)

        self.Fit()

    def menu_quit(self, event=None):
        self.Close()


if __name__ == "__main__":
    window = wx.App()
    frame = WindowFrame(None, title="soVx")
    frame.Show()
    window.MainLoop()
