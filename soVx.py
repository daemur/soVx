import os
import wx
from wx import py
import re
import math
import json
import time
import VxSim
import pyvx

class WindowPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        '''Panel containing all main contents of soVx window'''
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.Vx = WindowVx(self)
        self.parent = parent
        self.truck_selection = ''
        self.simulating = False
        self.config_path = os.path.expanduser('~/soVx.json')

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
        self.t_search_term = wx.TextCtrl(self, size = (100, 23))
        self.t_automate_end = wx.TextCtrl(self, size = (40, 23))

        # Buttons and bindings
        # TODO: Add tooltips and Error messages on incorrect input
        self.b_browse_config = wx.Button(self, label = '...', size = (20, 20))
        self.b_browse_config.Bind(wx.EVT_BUTTON, self.browse_config)

        self.b_browse_scene = wx.Button(self, label = '...', size = (20, 20))
        self.b_browse_scene.Bind(wx.EVT_BUTTON, self.browse_scene)
        self.b_browse_gtm = wx.Button(self, label = '...', size = (20, 20))
        self.b_browse_gtm.Bind(wx.EVT_BUTTON, self.browse_gtm)

        self.b_browse_scenario = wx.Button(self, label = '...', size = (20, 20))
        self.b_browse_scenario.Bind(wx.EVT_BUTTON, self.browse_scenario)

        self.b_browse_mechanism = wx.Button(self, label = '...', size = (20, 20))
        self.b_browse_mechanism.Bind(wx.EVT_BUTTON, self.browse_mechanism)

        self.b_start = wx.Button(self, label = 'Load Scene')
        self.b_start.Bind(wx.EVT_BUTTON, self.file_loader)

        self.b_step = wx.Button(self, label = 'Simulate')
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

        hsizer8.Add(self.b_start, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        # Load vertical sizer and all horizontal sizers it contains.
        self.SetSizerAndFit(vsizer)
        self.load_cfg()
    
    def save_cfg(self):
        try:
            d = {}
            d['config'] = self.t_config.GetValue()
            d['scene'] = self.t_scene.GetValue()
            d['gtm'] = self.t_gtm.GetValue()
            d['scenario'] = self.t_scenario.GetValue()
            d['mechanism'] = self.t_mechanism.GetValue()
            with open(self.config_path, 'w') as f:
                json.dump(d, f)
        except:
           pass

    def load_cfg(self):
        try:
            with open(self.config_path, 'r') as f:
                d = json.load(f)
                self.t_config.SetValue(d['config'])
                self.t_scene.SetValue(d['scene'])
                self.t_gtm.SetValue(d['gtm'])
                self.t_scenario.SetValue(d['scenario'])
                self.t_mechanism.SetValue(d['mechanism'])

        except:
            pass

    def browse(self, txt, wildcard):
        '''Opens a file browser in cwd.'''
        path = None
        if txt.GetValue():
            path = os.path.split(txt.GetValue())[0]
        if not path:
            path = os.getcwd()
        
        dlg = wx.FileDialog(
                self, message = 'Choose a file to load',
                defaultDir = path,
                defaultFile = '',
                wildcard = wildcard,
                style = wx.OPEN
                )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            if paths:
                txt.SetValue(paths[0])
                    
        dlg.Destroy()

    def browse_config(self, event):
        self.browse(self.t_config, ('*.vxc'))
        self.save_cfg()

    def browse_scene(self, event):
        self.browse(self.t_scene, ('*.vxs'))
        self.save_cfg()

    def browse_gtm(self, event):
        self.browse(self.t_gtm, ('*.vxm'))
        self.save_cfg()
        
    def browse_scenario(self, event):
        self.browse(self.t_scenario, ('*.json'))
        self.save_cfg()

    def browse_mechanism(self, event):
        self.browse(self.t_mechanism, ('*.vxm'))
        self.save_cfg()
    
    def scene_setup(self):
        '''Additional scene setup
           TODO: replace the junk in here with legitmate setup.'''
        try:
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
        except:
            pass

        # Disable the sun due to issue with shaders. Create and add ambient light.
        #env = self.Vx.scene.findExtension('PTLenEnvironment')
        #env.findExtension('SilverLining').getParameter('Sun Enabled').setValue(False)
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
        '''Steps and pauses the scene.'''
        print(self.simulating)
        if self.simulating:
            self.simulating = False
            self.b_step.SetLabel('Simulate')
        else:
            self.simulating = True
            self.b_step.SetLabel('Pause')
            while self.simulating:
                self.Vx.sim_app.update()
                wx.Yield()

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

    def truck_position(self):
        if self.truck_selection in ('BombCart'):
            self.truck_x = self.Vx.truck.findExtension('Bomb_Cart').getInput('Position').toVector3().toPyVxVector().x
            self.truck_y = self.Vx.truck.findExtension('Bomb_Cart').getInput('Position').toVector3().toPyVxVector().y
            self.truck_z = self.Vx.truck.findExtension('Bomb_Cart').getInput('Position').toVector3().toPyVxVector().z
            self.trans_truck = VxSim.VxTransform().makeRotationFromEulerAngles(VxSim.VxEulerAngles(0, 0, 90 * math.pi / 180))\
            * VxSim.VxTransform().makeTranslation(pyvx.Vector(self.truck_x, self.truck_y, self.truck_z + 2.0))
        if self.truck_selection in ('Chassis'):
            self.truck_x = self.Vx.truck.findExtension('Chassis').getInput('Position').toVector3().toPyVxVector().x
            self.truck_y = self.Vx.truck.findExtension('Chassis').getInput('Position').toVector3().toPyVxVector().y
            self.truck_z = self.Vx.truck.findExtension('Chassis').getInput('Position').toVector3().toPyVxVector().z
            self.trans_truck = VxSim.VxTransform().makeRotationFromEulerAngles(VxSim.VxEulerAngles(0, 0, 90 * math.pi / 180))\
            * VxSim.VxTransform().makeTranslation(pyvx.Vector(self.truck_x, self.truck_y, self.truck_z + 2.0))
        else:
            pass
    
    def do(self, it, timeout):
        start = time.clock()
        while not it():
            if timeout:
                if time.clock() - start > timeout:
                    print('timeout')
                    return False
                
            self.Vx.sim_app.update()
        return True

    def do_sequence(self, these):
        for those in these:
            print(those)
            if not self.do(*those):
                return False
        return True

    def move_liftables(self, event=None):
        '''Iterate through Vx.lift_objects list and apply the transform to the truck position.
        TODO: Create a while that can handle multiple truck positions.'''
        
        self.truck_position()
        original_position = (abs(self.truck_x), abs(self.truck_y), abs(self.truck_z))
        
        def current_position():
            return (abs(self.truck_x), abs(self.truck_y), abs(self.truck_z))

        for i in range(int(self.t_automate_end.GetValue())):

            print ('Moving container {0} of {1}').format(i + 1, int(self.t_automate_end.GetValue()))
            
            self.truck_position()
            print ('original: {0}\ncurrent: {1}').format(original_position[1], current_position()[1])
        
            def arrived():
                return int(current_position()[1]) < int(original_position[1]) * 1.05 and int(current_position()[1]) > int(original_position[1]) * .95
                
            def move():
                self.Vx.sim_app.getContentDispatcher().getMechanism(self.Vx.lift_objects[i]).findInterface('Liftable').getInput('Enable Attachment').setValue(False)
                self.Vx.sim_app.getContentDispatcher().getMechanism(self.Vx.lift_objects[i]).setTransform(self.trans_truck)
                del self.Vx.lift_objects[i]
                return True
        
            def leave():
                return int(current_position()[1]) > int(original_position[1]) * 1.05 or int(current_position()[1]) < int(original_position[1]) * .95
            
            if not self.do_sequence(((arrived, 30), (move, None), (leave, 15))):
                print('Error moving container {0} of {1}').format(i + 1, int(self.t_automate_end.GetValue()))
                break             
                
        #print('Error moving container number {0}. The truck did not arrive within 30 seconds.').format(i + 1)
        #return False
        #print('Error moving container number {0}. The truck did leave with the container within 5 seconds.').format(i + 1)
        #return False
                    
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
