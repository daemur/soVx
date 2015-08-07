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
        self.t_step_count = wx.TextCtrl(self, size = (40, 23))

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

        self.b_step = wx.Button(self, label = 'Step')
        self.b_step.Bind(wx.EVT_BUTTON, self.scene_step)

        # Place a ton of horizontal sizers within one expanding vertical sizer.
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer5 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer6 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer7 = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer1, .1, wx.EXPAND)
        vsizer.Add(hsizer2, .1, wx.EXPAND)
        vsizer.Add(hsizer3, .1, wx.EXPAND)
        vsizer.Add(hsizer4, .1, wx.EXPAND)
        vsizer.Add(hsizer5, .1, wx.EXPAND)
        vsizer.Add(hsizer6, .1, wx.ALIGN_RIGHT)
        vsizer.Add(hsizer7, .1, wx.ALIGN_RIGHT)

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

        hsizer6.Add(self.b_step, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer6.Add(self.t_step_count, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        hsizer7.Add(self.b_start, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
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
                str(self.t_scene.GetValue()), 'ContentExtensionScene'
                )
            self.Vx.sim_app.add(scene)
            self.Vx.scene = scene

    def scene_step(self, event=None):
        '''Steps the scene the selected number of times. 
        The soVx window will become unresponsive during this time.'''
        steps = int(self.t_step_count.GetValue())
        if steps is None:
            while True:
                self.Vx.sim_app.update()
        else:
            for i in range(0, steps):
                self.Vx.sim_app.update()

class WindowVx(WindowPanel):
    '''Exposed namespace to Pywrap. 
    All helper functions should be located here and can be called with the soVx.'''
    config = ''
    scene = ''
    gtm = ''
    scenario_json = ''
    mechanism = ''
    serializer = ''
    lift_objects = []
    truck = ''
    sim_app = VxSim.VxApplication()
      
    def __init__(self, *args, **kwargs):
        '''Create VxSim constants for contained functions.'''
    
    def vx_get_liftables(self, searchterm):
        self.lift_objects
        temp = []
        i = 0
    
        while app.getContentDispatcher().getMechanism(i) != None:
            x = app.getContentDispatcher().getMechanism(i)
            temp.append(x.getName())
            i += 1

        self.lift_objects = [ z for z, item in enumerate(temp) if re.search(searchterm, item)]

class WindowFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        '''Main frame holding "WindowPanel".'''
        wx.Frame.__init__(self, *args, **kwargs)

        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        port_menu = wx.Menu()

        construction_menu = wx.Menu()
         
        truck_submenu = wx.Menu()
        truck_submenu.Append(wx.ID_ANY, 'Trailer Chassis', kind = wx.ITEM_CHECK)
        truck_submenu.Append(wx.ID_ANY, 'Bomb Cart', kind = wx.ITEM_CHECK)
        port_menu.AppendMenu(wx.ID_ANY, '&Truck Type', truck_submenu)

        quit = file_menu.Append(wx.ID_EXIT, text='&Quit')
        self.Bind(wx.EVT_MENU, self.menu_quit, quit)

        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(port_menu, '&Port')
        menu_bar.Append(construction_menu, '&Construction')
        self.SetMenuBar(menu_bar)

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
    frame = py.crust.CrustFrame()
    frame.SetSize((750, 525))
    frame.Show(True)
    frame.shell.interp.locals['app'] = app
    app.MainLoop()

if __name__ == "__main__":
    app = soVx_main()
    soVx = WindowVx()
    wrap(app)
