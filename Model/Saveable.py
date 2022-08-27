import json as js
import os


# Saveable class for saving an object data to json file

class Saveable:

    def _store_data(self, file_name, data):
        with open(file_name, 'w') as file:
            js.dump(data, file)
    
    def _retrieve_data(self, file_name):
        data = []

        if os.path.exists(file_name):
            with open(file_name) as file:
                try:
                    data = js.load(file)
                except Exception as e:
                    pass
            
        return data


