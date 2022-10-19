import os, sys
import ctypes as cp

from .Core import SDM, QUEUE, PLATFORMS, CATEGORY


def open_file(_dir):
    if os.path.exists(_dir):
        os.startfile(_dir)


def turn_off(method, force = False):
    cmd = SDM.COMMANDS[method][sys.platform]

    if cmd:
        if method == QUEUE.PROCESS.POST.SHUT_DOWN and force:
            cmd += '/f'
        
        os.system(cmd)



def is_admin():
    try:
        return bool(cp.windll.shell32.IsUserAnAdmin())
    except:
        return False


# check os specific procedure for each method
# e.g : in windows for sleeping, first we need to turn off the hibernate
def check_os(method):

    result = True

    if sys.platform == PLATFORMS.WINDOWS:
        if method == QUEUE.PROCESS.POST.SLEEP:
            result = toggle_hibernate(False)
        elif method == QUEUE.PROCESS.POST.HIBERNATE:
            result = toggle_hibernate(True)
        
    return result


def toggle_hibernate(state = False):
    cmd = 'powercfg -hibernate '
    st = 'off'

    if state:
        st = 'on'
    
    return run_as(cmd + st)


# run command as administrator
def run_as(command):
    r = cp.windll.shell32.ShellExecuteW(None, 'runas', 'cmd.exe', '/c ' + command, None, 1)
    return r >= 32


# remove a directory from system
def remove_dir(path, delete_root = True):

    if os.path.exists(path) and os.path.isdir(path):
        entries = os.scandir(path)

        for e in entries:
            if e.is_file():
                os.remove(e)

        if delete_root:        
            os.rmdir(path)
    

def remove_file(path):
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)


# create temporary directory for a task
def makeTempDir(folder_name):
    path = os.path.join(SDM.PATHS.TEMP_PATH, folder_name)

    if not os.path.exists(path):
        os.makedirs(path)

    return path


# check if app main folders exists or not
def check_essential_folders():
    paths = []

    for cat in CATEGORY.CATEGORIES:
        if not cat:
            continue
        
        path = os.path.join(SDM.PATHS.MAIN_PATH, cat)
        paths.append(path)

    paths.append(SDM.PATHS.APP_PATH)
    paths.append(SDM.PATHS.TEMP_PATH)
    paths.append(SDM.PATHS.STASH_PATH)
    paths.append(SDM.PATHS.CACHE_PATH)


    for path in paths:

        if not os.path.exists(path):
            os.makedirs(path)








