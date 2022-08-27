import re

from PyQt5 import QtCore

from Utility.Core import STATUS

from .Util import MItem


# Model for filtering tasks
class FilterModel(QtCore.QSortFilterProxyModel):
    def __init__(self, model):
        super().__init__()

        self.setSourceModel(model)
        self.setDynamicSortFilter(True)
        # self.setSortRole(MItem.PRIVATE_ROLE)
            
        self.name_pattern = None
        self.state = None
        self.status = None
        self.category = None
        self.queue = None

        self.min_date = None
        self.max_date = None

        # date              [SORT, FILTER]
        # size              [SORT]
        # category          [FILTER]
        # state             [FILTER]
        # name              [FILTER, SORT]
        

    def filterAcceptsRow(self, row, parent):
            
        index = self.sourceModel().index(row, 0, parent)
        info = index.data(MItem.PRIVATE_ROLE)

        if not info:
            return False

        result = True

        # boolean multiplication is almost like AND

        if self.category:
            result *= (info.category == self.category)

        if self.state:
            if isinstance(self.state, (list, tuple)):
                result *= (info.state not in self.state)
            else:
                result *= (info.state == self.state)

        if self.status != None:
            if self.status:
                result *= info.status.is_active()
            else:
                result *= info.status.is_error()


        if self.queue:
            result *= (info.queue == self.queue)

        if self.min_date and self.max_date:
            pass

        if self.name_pattern:
            search = re.search(self.name_pattern, info.name)
            result *= (search != None)

            
        return result
            

            
    def set_ext(self, pattern):
        self.name_pattern = pattern
        self.invalidateFilter()
            
    def set_category(self, category):
        self.category = category
        self.invalidateFilter()
    
    def set_state(self, state):
        self.state = state
        self.invalidateFilter()

    def set_status(self, status):
        self.status = status
        self.invalidateFilter()
        
    def set_min_date(self, date):
        self.min_date = date
        self.invalidateFilter()

    def set_max_date(self, date):
        self.max_date = date
        self.invalidateFilter()

    def set_queue(self, queue):
        self.queue = queue
        self.invalidateFilter()





