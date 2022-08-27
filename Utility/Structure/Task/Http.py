from Utility.Core import LINK_TYPE, HTTP

from .Base import Option, Metadata, Request


# Http inherited and customized of Task Base Classed



class HttpMetadata(Metadata):

    def __init__(self, _id, url):
        super().__init__(_id)
        self._type = LINK_TYPE.HTTP

        self.url = url
        self.code = None
        self.resume = False
        self.date = None
        self.etag = None

    def is_successful(self):
        return self.code and HTTP.RESPONSE.OK <= self.code < HTTP.RESPONSE.REDIRECT

    def __str__(self):
        return f'{self._id} -- {self.code}'



class MultiRequest:
    def __init__(self, _id):
        self._id = _id
        self.link_iter = None
    
    def get_id(self):
        return self._id

    def set_link_iter(self, link_iter):
        self.link_iter = link_iter



class HttpOption(Option):

    def __init__(self, _id):
        super().__init__(_id, LINK_TYPE.HTTP)

        self.name = None
        self.url = None
        self.size = 0
        self.part = None
        self.resume = False
        self.etag = None
        self.modified_date = None
        self.duplicate_number = None

        self.username = None
        self.password = None


# Link generator class for batch handling
class LinkGenerator:
    
    def __init__(self, url, start, end, zero_fill, user = None, password = None):
        self.url = url
        self.start = start
        self.end = end
        self.zero_fill = zero_fill
        self.auth = (user, password)

        self.is_number = isinstance(start, int)


    def request_iter(self):

        for _id, url in self.info_iter():
            request = self.__create_request(_id, url)

            yield request


    def info_iter(self):
        start = self.start
        end = self.end

        if not self.is_number:
            start = ord(start)
            end = ord(end)
        

        for value_id in range(start, end + 1):

            if self.is_number:
                value_id = str(value_id).zfill(self.zero_fill)
            else:
                value_id = bytes([value_id]).decode("utf-8")
            
            new_url = self.url.format(value_id)

            yield value_id, new_url


    def __create_request(self, _id, url):
        request = Request(_id, url, LINK_TYPE.HTTP)

        if self.auth:
            request.user = self.auth[0]
            request.password = self.auth[1]

        return request


