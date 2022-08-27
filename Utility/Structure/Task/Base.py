import datetime as dt


# Base Option class for initializing task
class Option:
    def __init__(self, _id, _type):
        self._id = _id
        self._type = _type

        self.metadata = False

        self.path = None
        self.queue = None
        self.category = None
        self.date = None

        self.downloaded = 0
        self.progress = 0
        self.state = 0

        self.options = {}

        self.down_limit = None


# Task info class for containing data for using between UI and Model
class TaskInfo:

    def __init__(self):
        self._id = None
        self.url = None
        self.name = None
        self.path = None
        self.queue = None
        self._type = None
        self.category = None
        self.date = None
        self.part = None

        self.state = None
        self.status = None

        self.metadata = False

        self.download_speed = 0
        self.upload_speed = 0
        self.progress = 0
        self.eta = 0

        self.downloaded = 0
        self.total_size = 0
        self.resume = False




class Metadata:
    def __init__(self, _id):
        self._id = _id
        self._type = None
        self.name = None
        self.size = 0
    
    def is_successful(self):
        return False




class Request:
    def __init__(self, _id, url, _type):
        self._id = _id
        self.url = url
        self._type = _type

        # http special attrs
        self.user = None
        self.password = None
    
    def get_id(self):
        return self._id
    
    def get_type(self):
        return self._type

    def has_auth(self):
        return bool(self.user and self.password)

    def __str__(self):
        return f'{self.get_id()} -- {self.url[:30]} -- {self._type} -- {self.user} -- {self.password}'



class ActionRequest:

    def __init__(self, _id, action):
        self._id = _id
        self.action = action
        self.data = None
    

    def get_id(self):
        return self._id
    
    def get_action(self):
        return self.action



class TaskStatus:

    def __init__(self, name, is_error = False, is_active = False):
        self.name = name
        self.data = None
        self.__error = is_error
        self.__active = is_active


    def is_error(self):
        return self.__error
    
    def is_active(self):
        return self.__active


    def __str__(self):
        text = f'{self.name}'

        if self.data :
            text = f'{text}({self.data})'
        
        return text



class File:

    def __init__(self, name, parent = None, size = -1, prio = -1, index = -1):
        super().__init__()
        
        self.name = name
        self.parent = parent
        
        self.size = size
        self.priority = prio
        self.index = index
        self.downloaded = 0


    # an special name for identifying index
    def full_path_name(self):

        path = self.name

        temp = self

        while temp.parent:

            path = os.path.join(temp.parent.name, path)

            temp = temp.parent

        return path


    def set_priority(self, p):
        self.priority = p

    def get_priority(self):
        return self.priority

    
    def get_index(self):
        return self.index

    def get_size(self):
        return self.size

    def get_progress(self):
        return round(self.downloaded / self.size, 4) * 100

    def set_downloaded(self, d):
        self.downloaded = d

    def is_selected(self):
        return self.priority > 0
    
    def get_name(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
    


class Folder:

    def __init__(self, name, parent):
        
        self.name = name
        self.parent = parent
        self.folders = []
        self.files = []

        self.temp_selected = True

    def add_folder(self, folders):
        
        if isinstance(folders,(list, tuple, set)):
            
            for folder in folders:
                folder.parent = self

            self.folders.extend(folders)

        else:
            folders.parent = self
            self.folders.append(folders)
            
        self.sort_children()


    def add_file(self, files):

        if isinstance(files, (list, tuple, set)):
            
            for file in files:
                file.parent = self
                
            self.files.extend(files)
            
            
        else:
            files.parent = self
            self.files.append(files)
            

        self.sort_children(False)

    

    def children_count(self):
        return len(self.folders) + len(self.files)

    def sort_children(self, folders = True):

        if folders:
            self.folders.sort(key = sort_func)
        else:
            self.files.sort(key = sort_func)

    def print_children(self, level = 0):

        print("   " * level, f"({self.name})")

        for folder in self.folders:
            folder.print_children(level + 1)

        for file in self.files:
            print("   " * (level + 1), file.name)


    def get_files(self):
        return self.files
    

    def get_folders(self):
        return self.folders

        
    

    def get_name(self):
        return self.name

    def get_size(self):
        total = 0

        for folder in self.folders:
            total += folder.get_size()
        
        for file in self.files:
            total += file.get_size()
        
        return total
            

    def is_selected(self):
        states = []

        for item in [*self.folders, *self.files]:
            st = item.is_selected()

            if st == None:
                return None
            else:
                if st not in states:
                    states.append(st)
                
                if len(states) == 2:
                    break
        
        if True in states and False in states:
            return None
        else:
            return all(states)


    def get_selected_stats(self):
        count = 0
        size = 0

        for folder in self.folders:
            item = folder.get_selected_stats()
            count += item[0]
            size += item[1]
        
        for file in self.files:
            if file.is_selected():
                count += 1
                size += file.get_size()
        
        return count, size


    def set_priority(self, p):
        for file in self.files:
            file.set_priority(p)

        for folder in self.folders:
            folder.set_priority(p)


    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name




# sort function for folder's children
def sort_func(data):
    
    name = data.name

    try:
        index = name.index(".")
        first = name[:index]
    
        if first.isnumeric():
            return first.zfill(2)
        else:
            return name[0]
    except:
        return name[0]
    





