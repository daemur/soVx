import os
import wx
from wx import py
import VxSim

class WindowPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        '''Panel containing all main contents of soVx window'''
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.Vx = WindowVx(self)
        self.parent = parent
        self.current_directory = os.getcwd()

        # Labels
        self.l_config = wx.StaticText(self, size = (80, 25), label = 'Config')
        self.l_scene = wx.StaticText(self, size = (80, 25), label = 'Scene')
        self.l_gtm = wx.StaticText(self, size = (80, 23), label = 'GTM')
        self.l_scenario = wx.StaticText(self, size = (80, 25), label = 'Scenario')
        self.l_mechanism = wx.StaticText(self, size = (80, 25), label = 'Mechanism')

        # Textboxes
        self.t_config = wx.TextCtrl(self, size = (400, 23), )
        self.t_scene = wx.TextCtrl(self, size = (400, 23))
        self.t_gtm = wx.TextCtrl(self, size = (400, 23))
        self.t_scenario = wx.TextCtrl(self, size = (400, 23))
        self.t_mechanism = wx.TextCtrl(self, size = (400, 23))

        # Buttons
        self.b_browse_config = wx.Button(self, label = '...', size = (20, 20))
        self.b_browse_config.Bind(wx.EVT_BUTTON, self.browse_file)

        self.b_browse_scene = wx.Button(self, label = '...', size = (20, 20))
        self.b_browse_scene.Bind(wx.EVT_BUTTON, self.browse_file)

        self.b_browse_gtm = wx.Button(self, label = '...', size = (20, 20))
        self.b_browse_gtm.Bind(wx.EVT_BUTTON, self.browse_file)

        self.b_browse_scenario = wx.Button(self, label = '...', size = (20, 20))
        self.b_browse_scenario.Bind(wx.EVT_BUTTON, self.browse_file)

        self.b_browse_mechanism = wx.Button(self, label = '...', size = (20, 20))
        self.b_browse_mechanism.Bind(wx.EVT_BUTTON, self.browse_file)

        self.b_start = wx.Button(self, label = 'Run')
        self.b_start.Bind(wx.EVT_BUTTON, self.file_loader)

        self.b_run = wx.Button(self, label = 'Step')
        self.b_run.Bind(wx.EVT_BUTTON, self.Vx.vx_step)

        # Place a ton of horizontal sizers within one expanding vertical sizer.
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer5 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer6 = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer1, .1, wx.EXPAND)
        vsizer.Add(hsizer2, .1, wx.EXPAND)
        vsizer.Add(hsizer3, .1, wx.EXPAND)
        vsizer.Add(hsizer4, .1, wx.EXPAND)
        vsizer.Add(hsizer5, .1, wx.EXPAND)
        vsizer.Add(hsizer6, .1, wx.ALIGN_RIGHT)

        # Position all objects within the panel.
        hsizer1.Add(self.l_config, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer1.Add(self.b_browse_config, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer1.Add(self.t_config, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        hsizer2.Add(self.l_scene, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer2.Add(self.b_browse_scene, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer2.Add(self.t_scene, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        hsizer3.Add(self.l_gtm, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer3.Add(self.b_browse_gtm, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer3.Add(self.t_gtm, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        hsizer4.Add(self.l_scenario, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer4.Add(self.b_browse_scenario, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer4.Add(self.t_scenario, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        hsizer5.Add(self.l_mechanism, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer5.Add(self.b_browse_mechanism, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer5.Add(self.t_mechanism, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        hsizer6.Add(self.b_start, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        hsizer6.Add(self.b_run, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        
        # Load vertical sizer and all horizontal sizers it contains.
        self.SetSizerAndFit(vsizer)
        
    #def show_message_dlg(self, msg, title, style):
    #    '''Opens a message dialog'''
    #    dialog = wx.MessageDialog(parent=None, message=msg, 
    #                           caption=title, style=style)
    #    dialog.ShowModal()
    #    dialog.Destroy()
    
    #def error_msg(self, event):
    #    '''Warning message displayed when file of invalid type is selected'''
    #    self.show_message_dlg('Please select a file of a valid type. These include: *.vxc, *.vxs, *.json, *.vxm.',
    #                        'Filetype Error',
    #                        wx.OK | wx.ICON_INFORMATION
    #                        )
        
    def browse_file(self, event):
        '''Opens a file browser in cwd.
            TODO: Add error message dialog that doesnt whine all the time.
            TODO: Handle multiple files ending in .vxm (GTM and Mechanism).'''
          
        dlg = wx.FileDialog(
                self, message = 'Choose a file to load',
                defaultDir = self.current_directory,
                defaultFile = '',
                style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                if str(path).endswith('.vxc'):
                    self.t_config.SetValue(path)
                if str(path).endswith('.vxs'):
                    self.t_scene.SetValue(path)
                if str(path).endswith('.vxm'):
                    self.t_gtm.SetValue(path)
                if str(path).endswith('.json'):
                    self.t_scenario.SetValue(path)
                #if str(path).endswith('.vxs'):
                #    if self.Vx.files.get('mechanism') != None:
                #        del self.Vx.files['mechanism']
                #    self.Vx.files['mechanism'] = self.t_mechanism.SetValue(path)
                #    self.t_mechanism.SetValue(path)
          
        dlg.Destroy()

    def file_loader(self, event=None):
        '''Loads the scene into SimApp with selected files'''
        
        if  self.t_config.GetValue() != None:
            serializer = VxSim.VxApplicationConfigSerializer()
            serializer.load(str(self.t_config.GetValue()))
            
            if serializer.isValid():
                config = serializer.getApplicationConfig()
                config.apply(self.Vx.sim_app)
                self.Vx.config = config

        if self.t_scene.GetValue() != '':
            scene = self.Vx.sim_app.getSimulationFileManager().loadScene(
                str(self.Vx.t_scene.GetValue()), 'ContentExtensionScene'
                )
            self.Vx.sim_app.add(scene)
            self.Vx.scene = scene

'''
     # Light

key = VxFactoryKey.createFromUuid('6433097e-487e-5516-a47b-481abfdcc891')
light = VxExtensionFactory.create(key)
app.add(light)

# Scene

step(100)

scene = app.getSimulationFileManager().loadScene(STS, 'ContentExtensionScene')
app.add(scene)

# GTM
gtm_holder = app.getSimulationFileManager().loadMechanism(GTM)
gtm = gtm_holder.findExtension('GTM')
gtm_content = gtm_holder.findExtension('GTM Content')
gtm_content.getParameter('Mission File').setValue(SCENARIO)
gtm.getOutput('Use Bomb Cart').setValue(True)
gtm.getOutput('Use Trailer Chassis').setValue(False)

cms = app.getSimulationFileManager().loadMechanism('A:/builds/PTLEN/assets/Stage/assets/Environment/Objects/ContainerManagementSystemDisplay/Physics/ContainerManagementSystemDisplay.vxm', 'CMS.Mechanism')

invisibleDropZone1 = app.getSimulationFileManager().loadMechanism(DROP_ZONE, 'InvisibleDropZone1')
invisibleDropZone2 = app.getSimulationFileManager().loadMechanism(DROP_ZONE, 'InvisibleDropZone2')
invisibleDropZone3 = app.getSimulationFileManager().loadMechanism(DROP_ZONE, 'InvisibleDropZone3')
invisibleDropZone4 = app.getSimulationFileManager().loadMechanism(DROP_ZONE, 'InvisibleDropZone4')
'''

class WindowVx(WindowPanel):
    '''Exposed namespace to Pywrap. 
    All helper functions should be located here and can be called with the soVx constructor.'''
    config = ''
    scene = ''
    gtm = ''
    scenario_json = ''
    mechanism = ''
    serializer = ''
    lift_objects = ''
    truck = ''
    sim_app = VxSim.VxApplication()
        
    def __init__(self, *args, **kwargs):
        '''Create VxSim constants for contained functions.'''

    def vx_step(self, event=None):
        '''Steps the scene the selected number of times. 
        The soVx window will become unresponsive during this time.'''
        for i in range(0, 1000):
            self.sim_app.update()

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

class soVx_main(wx.App):
    def OnInit(self):
        frame = WindowFrame(None, title="soVx")
        frame.Show()
        return True

def wrap(app):
    wx.InitAllImageHandlers()
    frame = py.crust.CrustFrame()
    frame.SetSize((750, 525))
    frame.Show(True)
    frame.shell.interp.locals['app'] = app
    app.MainLoop()

if __name__ == "__main__":
    app = soVx_main()
    soVx = WindowVx()
    wrap(app)
