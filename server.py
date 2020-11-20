import pprint
import sys
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2

from quart import Quart, websocket, jsonify as j
app = Quart(__name__)





import pythoncom
import win32com.client as client
import pyvda


pythoncom.CoInitialize()

from pywinauto import backend
def entries(x):
    return {repr(x): repr(y) for x, y in vars(x).items()}

def details(element_info):
    return dict([
        ["zchildren", [details(child) for child in element_info.children()]],
        ["control_type", str(element_info.control_type)],
        ["name", str(element_info.name)],
        ['control_id', str(element_info.control_id)],
        ['class_name', str(element_info.class_name)],
        ['enabled', str(element_info.enabled)],
        ['handle', str(element_info.handle)],
        ['name', str(element_info.name)],
        ['process_id', str(element_info.process_id)],
        ['rectangle', str(element_info.rectangle)],
        ['rich_text', str(element_info.rich_text)],
        ['visible', str(element_info.visible)],
        ['automation_id', str(element_info.automation_id)],
        ['control_type', str(element_info.control_type)],
        ['element', str(element_info.element)],
        ['framework_id', str(element_info.framework_id)],
        ['runtime_id', str(element_info.runtime_id)],
    ])
def simpledetails(element_info):
    return dict([
        #["control_type", str(element_info.control_type)],
        ["automation_id", str(element_info.automation_id)],
        ["name", str(element_info.name)],
        #['class_name', str(element_info.class_name)],
        #['name', str(element_info.name)],
        #['process_id', str(element_info.process_id)],
        # ['rectangle', str(element_info.rectangle)],
    ])

@app.route('/fulltree')
async def fulltree():
    root = backend.registry.backends["uia"].element_info_class()
    return j(details(root))

@app.route('/overview')
async def overview():
    root = backend.registry.backends["uia"].element_info_class()
    taskbar_, = [element for element in root.children()
                if element.class_name == "Shell_TrayWnd"
                and element.name.lower().strip() == "taskbar"]
    tasks, = [element for element in taskbar_.children()
                if element.control_type == "ToolBar"
                and element.name.lower().strip() == "running applications"]
    taskbar  = [simpledetails(element) for element in tasks.children()]



    iconview, = [element for element in taskbar_.children()
              if element.class_name == "TrayNotifyWnd"]
    syspager, = [element for element in iconview.children()
                 if element.class_name == "SysPager"]
    toolbarwindow, = [element for element in syspager.children()
                 if element.control_type == "ToolBar"]
    icons = [simpledetails(element) for element in toolbarwindow.children()]

    windows = [simpledetails(element) for element in root.children()]
    return j({
        #"desktopnumber": desktopnumber,
        "root": root.name,
        "taskbar": taskbar,
        #"icons": icons,
        #"windows": windows,

    })
