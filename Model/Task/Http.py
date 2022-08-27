from Utility.Core import LINK_TYPE, SAVES
from Utility.Util import add_file_number

from .Base import BaseTask


class HttpTask(BaseTask):
    
    def __init__(self, _id):
        super().__init__(_id)

        self.set_type(LINK_TYPE.HTTP)

        self.down_limit = -1
        self.__duplicate_number = None

        

    def setup(self, options):
        super().setup(options)

        self.set_metadata(options.metadata)

        self.set_size(options.size)
        self.set_resume(options.resume)
        self.set_etag(options.etag)
        self.set_part(options.part)

        if not self.get_url():
            self.set_url(options.url)

        if not self.get_name():
            self.__duplicate_number = options.duplicate_number
            
            if options.metadata:
    
                name = options.name
                if self.__duplicate_number:
                    name = add_file_number(name, self.__duplicate_number)

                self.set_name(name)



    def get_url(self):
        return self.info.url

    def set_url(self, url):
        self.info.url = url

    def get_part(self):
        return self.info.part

    def set_part(self, part):
        self.info.part = part

    def get_etag(self):
        return self.info.etag
    
    def set_etag(self, new_etag):
        self.info.etag = new_etag

    def is_resumeable(self):
        return self.info.resume
    
    def get_modified_date(self):
        pass
    
    def set_down_limit(self, value):
        self.down_limit = value
    
    def get_down_limit(self):
        return self.down_limit



    def _get_save_data(self):
        data = super()._get_save_data()

        data[SAVES.SLOTS.TYPE] = self.get_type()

        data[SAVES.SLOTS.URL] = self.get_url()
        data[SAVES.SLOTS.PART] = self.get_part()
        data[SAVES.SLOTS.RESUME] = self.is_resumeable()
        data[SAVES.SLOTS.ETAG] = self.get_etag()

        # THESE SLOTS WILL BE ADDED IN FUTURE UPDATES AFTER EXAMINING
        # data['modified_date']
        # data['duplicate_number']

        return data






