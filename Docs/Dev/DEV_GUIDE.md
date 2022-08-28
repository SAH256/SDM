# Developer Guides

Before you start developing and put you time and energy for SDM check this sections:

- [Requirement](./DEV_GUIDE.md#requirement)
- [Build](./DEV_GUIDE.md#building)
- [Code style](./DEV_GUIDE.md#code-style)




## Requirement

If you tested the project and like to assist and contribute to it then read this first:

This project has 4 main requirements:
- [Python](./DEV_GUIDE.md#python)
- [PyQt5](./DEV_GUIDE.md#python-packages)
- [HTTPX](./DEV_GUIDE.md#python-packages)
- [Libtorrent](./DEV_GUIDE.md#libtorrent)

### Python
Well it is obvious to say that project has written in python, but you need python 3.8 version or newer for the shared library handling and building executable file for OS's olders versions like Windows 7. visit [here](https://www.python.org/downloads/release/python-385/).

### Python packages
All of these are in `requirement.txt` in the `Deps` folder. You only need to run this on cmd or terminal:

On the project root path: <br>
`pip install -r Deps/requirement.txt`



### Libtorrent
Be aware that Libtorrent library is not original python library that can be find in PyPi. You need to download the source and build it for your python version yourselves. for more information visit [here](https://libtorrent.org/building.html).


> While building the libtorrent it is up to you to build it in `static` or `shared` link library. In the project root folder there is a **Deps** folder which has the shared libraries of libtorrent and its dependecies based on build architecture. If you have built libtorrent both **static** in `link` and `runtime-link` then you don't need `Deps` folder. But if you have built it `shared` you need to add these dependencies as well :
> - torrent-rasterbar (libtorrent shared library)
> - libssl and libcrypto (openssl shared libraries)
> - boost-python (one of the shared libraries of boost)

> For the sake of launch speed build libtorrent **shared**.


**If you are confused _like me :(_, feel free to contact me, I will help you as much as I can.**


## Building

For building the project to executable file, I recommend `pyinstaller` package for simple and easy solution. 
There is a `SDM.spec` file in the root folder that you can pass to `pyinstaller` to do it.

Run this in the terminal on the root folder:
`pyinstaller SDM.spec`

You can find the compiled project in the **dist** folder.




## Code style

The project uses both python libraries and c++ binding packages of libtorrent and PyQt5 so, you are free to choose between **camelCase** or **snake_case** style. Also GUI project must follow MVC design pattern as much as possible for maintaining and easyness. please follow these rules for integrity of entire project:

### General rules

- Logic and main interactions with libraries must be in *Model*.
- GUI design and control must be in *UI*.
- Helping functions and data structures must be in *Utility*
- Const variables that is using across two or more files must put in ***Utility/Core.py***
- Graphic files like images must added to assets folder


### Model rules

-- Follow OOP and create seperate files for any structures or important class.
-- Each feature must have seperate folder like : *Task*, *Scheduler* and ...
-- Put Model only helping functions in *Model/Util.py*
-- ....


### UI rules
SDM GUI has built by handwritten desing code. For MVC approach the project uses waterfall system. For any GUI components first make `XXXUI.py` for UI sections. Then create `XXXControl.py` for controlling UI and communicating with Model.


-- Use base control widgets that is in *UI/Base*
-- For transfering data between UI and Model add PyQt Signal/Slot system in Control file
-- Seperate *Main* UI components with *Torrent* special UI and *Base widgets*
-- In UI programming follow other UI files for sample
-- If depth of UI goes beyond two underscore (like *__button()*) then create independent widget and add it to component folder of current developing widgets.
-- ...


### Utility rules

-- Don't put any UI or Model code in utility, only helping functions
-- Put data structures data in *Utility/Structure*
-- Put OS specific funtions in *Utility/Actions*
-- Put helping functions in appropriate file






