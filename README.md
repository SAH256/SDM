# SDM - Simple Download Manager powered by Python

SDM is a python based download manager that uses **[HTTPX](https://www.python-httpx.org)** for HTTP protocols and **[Libtorrent](https://www.libtorrent.org)** python binding for downloading torrents. All of these features bounded by a GUI app which uses **[PyQt5](https://doc.qt.io/qtforpython-5/)** library.

All these technologies leads to a software which is:
- Cross Platform
- User Friendly
- and Open Source
	

More features:
- Supports Http(s), Http2
- Supports Magnet Link and Torrent file
- Http Batch download
- Queue system and timer scheduling
- Torrent status panel
- Multi segment download
- Category and status filtering
- and More...

	
**Screenshots:**
<!-- most upload images here -->
![scr_1](https://user-images.githubusercontent.com/59185676/187040627-8e0e060b-526d-4c4c-86bb-d2a356112dd1.JPG)
![scr_2](https://user-images.githubusercontent.com/59185676/187040673-306f2b9f-c7ce-44cc-b41e-addd423aa240.JPG)
![scr_3](https://user-images.githubusercontent.com/59185676/187040716-e4f2b6a9-1119-4be8-8fbe-a700e7600c43.JPG)
![scr_4](https://user-images.githubusercontent.com/59185676/187040740-3612054d-08f7-4005-8359-d15c9e86310e.JPG)
![scr_5](https://user-images.githubusercontent.com/59185676/187040760-f7705743-496e-400c-944a-000704f5a7eb.JPG)
![scr_6](https://user-images.githubusercontent.com/59185676/187040851-b5dc1abe-56f3-4467-8e73-00d72c87bbe2.JPG)
![scr_7](https://user-images.githubusercontent.com/59185676/187040837-e20f3006-dcbc-42dd-a6af-11d3118715ff.JPG)
![scr_8](https://user-images.githubusercontent.com/59185676/187040880-b1239fca-d5f0-48ab-a939-56a78d78fdd1.JPG)




The only thing that is missed, is your supports and cooperations. The project is currently under development and it is far away to become complete. It still can do basic downloading and scheduling actions so don't worry when using it. Feel free to use, distribute and introduce this project.


## Downloads

You can get a compressed file of compiled executable of project. It only works with ***MS Windows 64bit *** for now But, in future we will build for other OSs and architectures.
extract it and in the extracted folder run **SDM.exe**. 

[Download for AMD64](https://drive.google.com/file/d/1hTolJxtfr2J89tiJ51Rdf5-SU8ljc0lm/view?usp=drivesdk)



## Contribution

If you tested the project and like to assist and contribute to it then read this first:

This project has 4 main requirements:
- [Python](https://github.com/SAH256/SDM/edit/main/README.md#python)
- [PyQt5](https://github.com/SAH256/SDM/edit/main/README.md#python-packages)
- [HTTPX](https://github.com/SAH256/SDM/edit/main/README.md#python-packages)
- [Libtorrent](https://github.com/SAH256/SDM/edit/main/README.md#libtorrent)

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






