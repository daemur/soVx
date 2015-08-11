import os
import wx
from wx import py
import re
import math
import VxSim
import pyvx

class WindowPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        '''Panel containing all main contents of soVx window'''
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.Vx = WindowVx(self)
        self.parent = parent
        self.current_directory = os.getcwd()
        self.truck_selection = ''

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
        self.t_search_term = wx.TextCtrl(self, size = (100, 23))
        self.t_automate_end = wx.TextCtrl(self, size = (40, 23))

        # Buttons and bindings
        # TODO: Add tooltips and Error messages on incorrect input
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

        self.b_start = wx.Button(self, label = 'Load Scene')
        self.b_start.Bind(wx.EVT_BUTTON, self.file_loader)

        self.b_step = wx.Button(self, label = 'Step')
        self.b_step.Bind(wx.EVT_BUTTON, self.scene_step)

        self.b_search = wx.Button(self, label = 'Search')
        self.b_search.Bind(wx.EVT_BUTTON, self.get_liftables)

        self.b_automate = wx.Button(self, label = 'Automate to:')
        self.b_automate.Bind(wx.EVT_BUTTON, self.move_liftables)

        # Place a ton of horizontal sizers within one expanding vertical sizer.
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer5 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer6 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer7 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer8 = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer1, .1, wx.EXPAND)
        vsizer.Add(hsizer2, .1, wx.EXPAND)
        vsizer.Add(hsizer3, .1, wx.EXPAND)
        vsizer.Add(hsizer4, .1, wx.EXPAND)
        vsizer.Add(hsizer5, .1, wx.EXPAND)
        vsizer.Add(hsizer6, .1, wx.EXPAND)
        vsizer.Add(hsizer7, .1, wx.ALIGN_RIGHT)
        vsizer.Add(hsizer8, .1, wx.ALIGN_RIGHT)

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

        hsizer6.Add(self.b_search, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer6.Add(self.t_search_term, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer6.Add(self.b_automate, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer6.Add(self.t_automate_end, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        hsizer7.Add(self.b_step, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer7.Add(self.t_step_count, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        hsizer8.Add(self.b_start, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
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
            TODO: Handle multiple files ending in .vxm (GTM and Mechanism). Get UUID of object.'''
          
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
          
        dlg.Destroy()
    
    def scene_setup(self):
        '''Additional scene setup
           TODO: replace the junk in here with legitmate setup.'''
        self.Vx.invisibleDropZone1 = self.Vx.sim_app.getSimulationFileManager().loadMechanism(
            'a:/builds/PTLEN/assets/STAGE/assets/Environment/Objects/InvisibleDropZone/Physics/InvisibleDropZone.vxm',
            'InvisibleDropZone1')
        self.Vx.invisibleDropZone2 = self.Vx.sim_app.getSimulationFileManager().loadMechanism(
            'a:/builds/PTLEN/assets/STAGE/assets/Environment/Objects/InvisibleDropZone/Physics/InvisibleDropZone.vxm',
            'InvisibleDropZone2')
        self.Vx.invisibleDropZone3 = self.Vx.sim_app.getSimulationFileManager().loadMechanism(
            'a:/builds/PTLEN/assets/STAGE/assets/Environment/Objects/InvisibleDropZone/Physics/InvisibleDropZone.vxm',
            'InvisibleDropZone3')
        self.Vx.invisibleDropZone4 = self.Vx.sim_app.getSimulationFileManager().loadMechanism(
            'a:/builds/PTLEN/assets/STAGE/assets/Environment/Objects/InvisibleDropZone/Physics/InvisibleDropZone.vxm',
            'InvisibleDropZone4')
      
        self.Vx.cms = self.Vx.sim_app.getSimulationFileManager().loadMechanism(
            'A:/builds/PTLEN/assets/Stage/assets/Environment/Objects/ContainerManagementSystemDisplay/Physics/ContainerManagementSystemDisplay.vxm',
            'CMS.Mechanism')

        # Disable the sun due to issue with shaders. Create and add ambient light.

        key = VxSim.VxFactoryKey.createFromUuid('6433097e-487e-5516-a47b-481abfdcc891')
        light = VxSim.VxExtensionFactory.create(key)
        self.Vx.sim_app.add(light)


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
            self.scene = self.Vx.sim_app.getSimulationFileManager().loadScene(
                str(self.t_scene.GetValue()), 'ContentExtensionScene'
                )
            self.Vx.sim_app.add(self.scene)
            self.Vx.scene = self.scene

        if self.t_gtm.GetValue() != '':
            gtm_holder = self.Vx.sim_app.getSimulationFileManager().loadMechanism(str(self.t_gtm.GetValue()))
            self.Vx.gtm = gtm_holder.findExtension('GTM')
            self.Vx.gtm_content = gtm_holder.findExtension('GTM Content')
            
            if self.truck_selection in ('BombCart'):
                try:
                    self.Vx.gtm.getOutput('Use Bomb Cart').setValue(True)
                    self.Vx.gtm.getOutput('Use Trailer Chassis').setValue(False)
                except AttributeError:
                    pass
            elif self.truck_selection in ('Chassis'):
                try:
                    self.Vx.gtm.getOutput('Use Bomb Cart').setValue(False)
                    self.Vxgtm.getOutput('Use Trailer Chassis').setValue(True)
                except AttributeError:
                    pass
            else:
                pass

            try:
                self.Vx.gtm.getOutput('Display CMS?').setValue(True)
            except AttributeError:
                pass

            if self.t_scenario.GetValue() != '':
                self.Vx.gtm_content.getParameter('Mission File').setValue(str(self.t_scenario.GetValue()))
            else:
                pass
    
        # TODO: clean this function and bug issues requiring workarounds.
        self.scene_setup()

        for i in range(0, 500):
            self.Vx.sim_app.update()
        
        self.get_sceneObjects()

    def scene_step(self, event=None):
        '''Steps the scene the selected number of times. 
        The soVx window will become unresponsive during this time.'''
        steps = int(self.t_step_count.GetValue())
        if steps is None:
            pass
        else:
            for i in range(0, steps):
                self.Vx.sim_app.update()

    def get_sceneObjects(self, event=None):
        '''Creates a list of scene objects and appends the to Vx.scene_objects.'''
        temp = []
        i = 0
    
        while self.Vx.scene.getSimObject(i) != None:
            x = self.Vx.scene.getSimObject(i)
            temp.append(x.getName())
            i += 1

        self.Vx.scene_objects = temp
        print(temp)

        for z in temp:
            if re.search('Bomb', z) or re.search('Chassis', z):
                self.Vx.truck = self.Vx.scene.getSimObject(temp.index(z))
                print(self.Vx.truck.getName())

    def get_liftables(self, event=None):
        '''Creates a list of objects from a searchterm and appends the to Vx.lift_objects.'''
        searchterm = str(self.t_search_term.GetValue())
        temp = []
        i = 0
        
        while self.Vx.sim_app.getContentDispatcher().getMechanism(i) != None:
            x = self.Vx.sim_app.getContentDispatcher().getMechanism(i)
            temp.append(x.getName())
            i += 1

        self.Vx.lift_objects = [ z for z, item in enumerate(temp) if re.search(searchterm, item)]

    def move_liftables(self, event=None):
        '''Iterate through Vx.lift_objects list and apply the transform to the truck position.
        TODO: Create a while that can handle multiple truck positions.'''
        
        if self.truck_selection in ('BombCart'):
            for current in range(int(self.t_automate_end.GetValue())):
                
                print ('Moving container {0} of {1}').format(current, int(self.t_automate_end.GetValue()))
                
                for i in self.Vx.lift_objects:

                    truck_x = self.Vx.truck.findExtension('Bomb_Cart').getInput('Position').toVector3().toPyVxVector().x
                    truck_y = self.Vx.truck.findExtension('Bomb_Cart').getInput('Position').toVector3().toPyVxVector().y
                    truck_z = self.Vx.truck.findExtension('Bomb_Cart').getInput('Position').toVector3().toPyVxVector().z
                    trans_truck = VxSim.VxTransform().makeRotationFromEulerAngles(VxSim.VxEulerAngles(0,0,90 * math.pi / 180))\
                    * VxSim.VxTransform().makeTranslation(pyvx.Vector(truck_x,truck_y,truck_z + 2.0))
                
                    self.Vx.sim_app.getContentDispatcher().getMechanism(i).setTransform(trans_truck)
                    self.Vx.sim_app.getContentDispatcher().getMechanism(i).findInterface('Liftable').getInput('Enable Attachment').setValue(False)
                    self.Vx.lift_objects.remove(i)

                    for x in range(0, 2500):
                        self.Vx.sim_app.update()
                    
        if self.truck_selection in ('Chassis'):
            for current in range(int(self.t_automate_end.GetValue())):
                for i in self.Vx.lift_objects:

                    print ('Moving container {0} of {1}').format(current, int(self.t_automate_end.GetValue()))
                    
                    truck_x = self.Vx.truck.findExtension('Chassis').getInput('Position').toVector3().toPyVxVector().x
                    truck_y = self.Vx.truck.findExtension('Chassis').getInput('Position').toVector3().toPyVxVector().y
                    truck_z = self.Vx.truck.findExtension('Chassis').getInput('Position').toVector3().toPyVxVector().z
                    trans_truck = VxSim.VxTransform().makeRotationFromEulerAngles(VxSim.VxEulerAngles(0,0,90 * math.pi / 180))\
                    * VxSim.VxTransform().makeTranslation(pyvx.Vector(truck_x,truck_y,truck_z + 1.8))

                    self.Vx.sim_app.getContentDispatcher().getMechanism(i).setTransform(trans_truck)
                    self.Vx.sim_app.getContentDispatcher().getMechanism(i).findInterface('Liftable').getInput('Enable Attachment').setValue(False)
                    self.Vx.lift_objects.remove(i)
                    
                    for x in range(0, 2500):
                        self.Vx.sim_app.update()

        else:
            pass

class WindowVx(WindowPanel):
    '''Exposed namespace to Pywrap. 
    All helper functions, not connected to the UI, should be located here and can be called with the soVx.'''
    sim_app = VxSim.VxApplication()
    config = None
    scene = None
    gtm = None
    gtm_content = None
    scenario_json = None
    serializer = None
    truck = None
    lift_objects = []
    scene_objects = []
      
    def __init__(self, *args, **kwargs):
        '''Create VxSim constants for contained functions.'''

class WindowFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        '''Main frame holding "WindowPanel".'''
        wx.Frame.__init__(self, *args, **kwargs)

        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        port_menu = wx.Menu()

        construction_menu = wx.Menu()
         
        truck_submenu = wx.Menu()
        self.truck_chassis = truck_submenu.Append(wx.ID_ANY, 'Trailer Chassis', kind = wx.ITEM_CHECK)
        self.truck_bombCart = truck_submenu.Append(wx.ID_ANY, 'Bomb Cart', kind = wx.ITEM_CHECK)
        port_menu.AppendMenu(wx.ID_ANY, '&Truck Type', truck_submenu)

        self.Bind(wx.EVT_MENU, self.truck_select, self.truck_chassis)
        self.Bind(wx.EVT_MENU, self.truck_select, self.truck_bombCart)
        
        quit = file_menu.Append(wx.ID_EXIT, text='&Quit')
        self.Bind(wx.EVT_MENU, self.menu_quit, quit)

        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(port_menu, '&Port')
        menu_bar.Append(construction_menu, '&Construction')
        self.SetMenuBar(menu_bar)

        self.Panel = WindowPanel(self)

        self.Fit()

    def menu_quit(self, event = None):
        self.Close()

    def truck_select(self, e):
        '''For port projects. Detwrmine truck type to load into the scene. Passes string to Panel.'''
        if self.truck_chassis.IsChecked():
            #self.truck_bombCart.SetValue(False)
            self.Panel.truck_selection = 'Chassis'
        if self.truck_bombCart.IsChecked():
            #self.truck_chassis.SetValue(False)
            self.Panel.truck_selection = 'BombCart'

class soVx_main(wx.App):
    '''wx.APP instance to be wrapped by pyCrust.'''
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
