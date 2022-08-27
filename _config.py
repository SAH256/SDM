import os

def add_dll_directory(path):
    
    if not os.path.isabs(path):
        path = os.path.abspath(path)

    if os.path.exists(path):
        os.add_dll_directory(path)


DEPS_FOLDER = 'Deps'
arch_attr = 'PROCESSOR_ARCHITECTURE'

arch = os.getenv(arch_attr)

path = os.path.join(DEPS_FOLDER, arch)

add_dll_directory(path)


