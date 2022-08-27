from PyQt5 import QtWidgets

from UI.Base.SpinBox.StyleSpinBoxControl import SpinBoxControl


# Setting Network section -- UI class
class NetworkUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.network_data = None

        self._spins()


    def _spins(self):
        parent_layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(parent_layout)


        spins = [
            ('max_con', 'Max Connection', (10, 5, 100)),
            ('default_part', 'Default Part', (10, 1, 32)),
        ]

        for item in spins:
            layout = QtWidgets.QHBoxLayout()
            parent_layout.addLayout(layout)

            label = QtWidgets.QLabel(item[1])
            wid = SpinBoxControl(*item[2])

            
            layout.addWidget(label)
            layout.addStretch(1)
            layout.addWidget(wid)

            setattr(self, item[0], wid)




    def set_data(self, data):
        self.network_data = data

        self.__setup()


    def __setup(self):
        self.max_con.set_value(self.network_data.get_max_connection())
        self.default_part.set_value(self.network_data.get_default_part())


    def apply_changes(self):
        conn_value = self.max_con.get_value()
        part_value = self.default_part.get_value()

        self.network_data.set_max_connection(conn_value)
        self.network_data.set_default_part(part_value)

