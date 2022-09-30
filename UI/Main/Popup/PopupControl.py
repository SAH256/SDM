from .Boxes.Add.AddUI import AddUI
from .Boxes.Duplicate.DuplicateUI import Duplicate
from .Boxes.Confirm.ConfirmUI import Confirm
from .Boxes.Delete.DeleteUI import Delete
from .Boxes.Torrent.TorrentUI import TorrentFile
from .Boxes.TextArea.TextAreaUI import TextEntry

from Utility.Core import POPUP_TYPE


# Popup initIalizing mechanism based on type


POPUP_DIALOGS = {
    POPUP_TYPE.ADD : AddUI,
    POPUP_TYPE.DUPLICATE : Duplicate,
    POPUP_TYPE.DELETE : Delete,
    POPUP_TYPE.CONFIRMATION : Confirm,
    POPUP_TYPE.TORRENT_FILE : TorrentFile,
    POPUP_TYPE.TEXTAREA : TextEntry,
}



def create_popup(parent, _type, title, state = None, data = None):
    wid = POPUP_DIALOGS.get(_type)
    result = None

    if wid:
        dialog = wid(parent)
        dialog.set_state(state)
        dialog.set_title(title)
        dialog.set_data(data)

        result = dialog.exec()
    
    return result






