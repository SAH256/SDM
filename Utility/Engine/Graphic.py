
import os, shutil as sh
from lxml import etree

SRC_PATH = 'src'
OUT_PATH = 'output'


# STYLESHEET = '''
#         path, circle,
#         rect, ellipse,
#         polygon {
#             fill : url(#color-1);
#         }

#         line, polyline {
#             stroke : url(#color-1);
#         }

#         .negative_path {
#             fill : #ff5613;
#         }

#         .positive_path {
#             fill : #0078d8;
#         }
# '''


# DATA = {
#     "Action" : {
#         'normal' : [(100, '#212121')],
#         'hover' : [
#             (0, '#00f2fe'),
#             (100, '#4facfe')
#             ]
#         },

#     "Files": None,

#     # "Files" : {
#     #     'normal' : [(100, '#212121')],
#     #     'disabled' : [
#     #         (100, '#888')
#     #         ]
#     #     },
# }


def create_element(tag_name, parent = None, index = 0):
    element = None
    
    if parent != None:
        element = parent.find(tag_name, parent.nsmap)
    
    if element == None:
        element = etree.Element(tag_name)
        element.tail = '\n\n\t'

        # if parent != None:
        #     parent.insert(index, element)
    
    return element


def apply_style(src, dest, style, colors, output = ''):

    for entry in os.scandir(src):
        if entry.is_file() and entry.name.endswith('.svg'):

            for state in colors:
                tree = change_stylesheet(entry.path, style, colors[state])
                
                name = entry.name
                
                if state:
                    name = f'{os.path.splitext(entry.name)[0]}-{state}.svg'

                save_path = os.path.join(dest, name)
                
                if tree != None:
                    save_file(save_path, tree)
    
        
def change_stylesheet(path, style, colors):
    try:
        tree = etree.parse(path)
        root = tree.getroot()
    except:
        print('Error => ', path)
        return
    
    _id = 'color-1'
    
    gradient = create_linear_gradient(_id, colors)

    defs = create_element('defs', root)
    defs.insert(0, gradient)
    
    element = create_element('style', defs)
    
    if element.text != None:
        element.text = style + "\n " + element.text
    else:
        element.text = style

    defs.insert(0, element)
    root.insert(0, defs)
    
    return tree



def save_file(save_path, tree):

    with open(save_path, 'wb') as file:
        tree.write(file, encoding = tree.docinfo.encoding, 
                         standalone = tree.docinfo.standalone, 
                         pretty_print = True, 
                         xml_declaration = True, 
                         strip_text = True)



def create_linear_gradient(_id, colors_data):
    lg = create_element('linearGradient')
    lg.set('id', _id)

    for index, data in enumerate(colors_data):
        stop = lg.makeelement('stop')
        stop.set('offset', f'{data[0]}%')
        stop.set('stop-color', data[1])
        lg.insert(index, stop)
        
        if index != len(colors_data) - 1:
            stop.tail = '\n\t\t'
        else:
            stop.tail = '\n\t'

    return lg



